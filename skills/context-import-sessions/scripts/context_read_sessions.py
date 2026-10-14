#!/usr/bin/env python3
"""List .context/sessions.log or record the review date of a session."""

import argparse
import csv
import datetime
import hashlib
import json
import os
import stat
import subprocess
import sys
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path

FIELDS = ("session_date", "session_id", "path", "reviewed_date")


@contextmanager
def queue_lock(directory):
    """Shared protocol for the independently installed hook and queue reader."""
    with (directory / ".sessions.lock").open("a+b") as handle:
        deadline = time.monotonic() + 1
        while True:
            try:
                if os.name == "nt":
                    import msvcrt
                    handle.seek(0)
                    msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except OSError:
                if time.monotonic() >= deadline:
                    raise TimeoutError("session queue is busy; retry later")
                time.sleep(0.02)
        try:
            yield
        finally:
            if os.name == "nt":
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle, fcntl.LOCK_UN)


def validate_row(row, source):
    if (set(row) != set(FIELDS)
            or any(not isinstance(value, str) for value in row.values())
            or not row["session_id"].strip() or not row["path"].strip()):
        raise ValueError("invalid session record: " + str(source))
    for field in ("session_date", "reviewed_date"):
        value = row[field]
        if field == "reviewed_date" and not value:
            continue
        try:
            if datetime.date.fromisoformat(value).isoformat() != value:
                raise ValueError()
        except ValueError:
            raise ValueError("invalid session date in " + str(source)) from None


def read_sessions(directory):
    """Read one snapshot of the current CSV log."""
    sessions = {}
    path = directory / "sessions.log"
    if not path.exists():
        return sessions
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle, strict=True)
        if next(reader, None) != list(FIELDS):
            raise ValueError("invalid session log header: " + str(path))
        for values in reader:
            if len(values) != len(FIELDS):
                raise ValueError("invalid session record: " + str(path))
            row = dict(zip(FIELDS, values))
            validate_row(row, path)
            if row["session_id"] in sessions:
                raise ValueError("duplicate session_id in session log: " + row["session_id"])
            sessions[row["session_id"]] = row
    return sessions


def write_sessions(path, sessions):
    """Write the log atomically, retrying one failed write under the caller's lock."""
    for row in sessions.values():
        validate_row(row, path)
    for attempt in range(2):
        try:
            write_sessions_once(path, sessions)
            return
        except OSError:
            if attempt == 1:
                raise
            time.sleep(0.05)


def write_sessions_once(path, sessions):
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="", dir=path.parent,
                                         suffix=".tmp", delete=False) as handle:
            temporary = Path(handle.name)
            writer = csv.writer(handle, lineterminator="\n")
            writer.writerow(FIELDS)
            for row in sessions.values():
                writer.writerow([row[field] for field in FIELDS])
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def checkpoint(row):
    """Detect changed record identity or transcript metadata without reading content."""
    signature = None
    if row["path"]:
        try:
            info = Path(row["path"]).stat()
            if stat.S_ISREG(info.st_mode):
                signature = [info.st_size, info.st_mtime_ns, info.st_ctime_ns]
        except FileNotFoundError:
            pass
    if signature is None:
        return None
    data = [row["session_date"], row["session_id"], row["path"], signature]
    return hashlib.sha256(json.dumps(data, ensure_ascii=False).encode("utf-8")).hexdigest()


def inventory(directory, session_id=None, expected_checkpoint=None):
    if not directory.exists():
        if session_id:
            raise ValueError("session is not in the queue")
        return {}
    if session_id is None:
        # The complete log is replaced atomically; listing needs no writer lock.
        return read_sessions(directory)
    with queue_lock(directory):
        sessions = read_sessions(directory)
        if expected_checkpoint is None:
            raise ValueError("--checkpoint is required when marking a review")
        if session_id not in sessions:
            raise ValueError("session is not in the queue")
        row = sessions[session_id]
        current = checkpoint(row)
        if current is None:
            raise ValueError("session transcript is unavailable; leave the review pending")
        if current != expected_checkpoint:
            raise ValueError("session checkpoint changed; review its new evidence first")
        if not row["reviewed_date"]:
            row["reviewed_date"] = datetime.date.today().isoformat()
            write_sessions(directory / "sessions.log", sessions)
        return sessions


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", type=Path)
    parser.add_argument("--mark-reviewed", metavar="SESSION_ID")
    parser.add_argument("--checkpoint", help="Exact checkpoint token printed before reading the transcript")
    args = parser.parse_args()
    if bool(args.mark_reviewed) != (args.checkpoint is not None):
        parser.error("--mark-reviewed and --checkpoint must be supplied together")
    try:
        result = subprocess.run(
            ["git", "-C", str(args.project_root.resolve()), "rev-parse", "--show-toplevel"],
            check=True, capture_output=True, text=True, timeout=1,
        )
        directory = Path(result.stdout.strip()) / ".context"
        sessions = inventory(directory, args.mark_reviewed, args.checkpoint)
        pending = [row for row in sessions.values() if not row["reviewed_date"]]
        lines = []
        for row in pending:
            transcript = row["path"]
            token = checkpoint(row)
            availability = "available" if token else "missing-file"
            lines.append("%s  %s  transcript=%s  checkpoint=%s  path=%s" % (
                row["session_id"], row["session_date"], availability, token or "-",
                json.dumps(transcript, ensure_ascii=False),
            ))
    except (OSError, ValueError, csv.Error, subprocess.SubprocessError) as exc:
        print("context-skills: could not inspect queue: %s" % exc, file=sys.stderr)
        return 2
    print("queued: %d, reviewed: %d, pending: %d" % (
        len(sessions), len(sessions) - len(pending), len(pending)))
    for line in lines:
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
