#!/usr/bin/env python3
"""List pending sessions with file sizes, or record a completed review."""

import argparse
import csv
import datetime
import json
import stat
import subprocess
import sys
from pathlib import Path

FIELDS = ("session_date", "session_id", "path", "reviewed_date")


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
    """Write the session log."""
    for row in sessions.values():
        validate_row(row, path)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(FIELDS)
        for row in sessions.values():
            writer.writerow([row[field] for field in FIELDS])


def inventory(directory, session_ids=None):
    if not directory.exists():
        if session_ids:
            raise ValueError("session is not in the queue")
        return {}
    if session_ids is None:
        # Listing does not modify the log.
        return read_sessions(directory)
    sessions = read_sessions(directory)
    selected = []
    for session_id in dict.fromkeys(session_ids):
        if session_id not in sessions:
            raise ValueError("session is not in the queue: " + session_id)
        row = sessions[session_id]
        if not Path(row["path"]).is_file():
            raise ValueError("session transcript is unavailable: " + session_id)
        if not row["reviewed_date"]:
            selected.append(row)
    if selected:
        review_date = datetime.date.today().isoformat()
        for row in selected:
            row["reviewed_date"] = review_date
        write_sessions(directory / "sessions.log", sessions)
    return sessions


def describe_session(row):
    """Report file metadata without selecting groups or reading transcript contents."""
    size, error = None, None
    try:
        info = Path(row["path"]).stat()
        availability = "available" if stat.S_ISREG(info.st_mode) else "missing-file"
        if availability == "available":
            size = info.st_size
    except FileNotFoundError:
        availability = "missing-file"
    except OSError as exc:
        availability, error = "unavailable", str(exc)
    line = "%s  %s  transcript=%s  bytes=%s  path=%s" % (
        row["session_id"], row["session_date"], availability,
        size if size is not None else "-",
        json.dumps(row["path"], ensure_ascii=False),
    )
    if error:
        line += "  error=" + json.dumps(error, ensure_ascii=False)
    return line


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", type=Path)
    parser.add_argument("--mark-reviewed", metavar="SESSION_ID", nargs="+")
    args = parser.parse_args()
    try:
        result = subprocess.run(
            ["git", "-C", str(args.project_root.resolve()), "rev-parse", "--show-toplevel"],
            check=True, capture_output=True, text=True, timeout=1,
        )
        directory = Path(result.stdout.strip()) / ".context"
        sessions = inventory(directory, args.mark_reviewed)
        pending = sorted((row for row in sessions.values() if not row["reviewed_date"]),
                         key=lambda row: (row["session_date"], row["session_id"]))
        lines = [describe_session(row) for row in pending]
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
