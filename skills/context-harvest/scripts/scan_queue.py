#!/usr/bin/env python3
"""Inventory session metadata in a project's .context/sessions directory."""

import argparse
import datetime
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def queue_dir(project):
    result = subprocess.run(
        ["git", "-C", str(project), "rev-parse", "--show-toplevel"],
        check=True, capture_output=True, text=True,
    )
    return Path(result.stdout.strip()) / ".context" / "sessions"


def read_sessions(state):
    sessions = {}
    for path in sorted(state.glob("*.json")):
        try:
            row = json.loads(path.read_text(encoding="utf-8"))
        except (ValueError, OSError) as exc:
            print("skipped unreadable session %s: %s" % (path, exc), file=sys.stderr)
            continue
        if isinstance(row, dict) and row.get("session_id") == path.stem:
            sessions[path.stem] = (path, row)
        else:
            print("skipped invalid session metadata: %s" % path, file=sys.stderr)
    return sessions


def mark_reviewed(path, row):
    row["reviewed_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                         suffix=".tmp", delete=False) as handle:
            temporary_path = Path(handle.name)
            json.dump(row, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(temporary_path, path)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", type=Path)
    parser.add_argument("--mark-reviewed", metavar="SESSION_ID")
    parser.add_argument("--queued-at", help="Only mark the checkpoint with this queued_at timestamp")
    args = parser.parse_args()
    try:
        state = queue_dir(args.project_root.resolve())
    except (OSError, subprocess.SubprocessError):
        print("project_root is not an accessible Git checkout", file=sys.stderr)
        return 2
    sessions = read_sessions(state)
    if args.mark_reviewed:
        if args.mark_reviewed not in sessions:
            print("session is not in the queue", file=sys.stderr)
            return 2
        path, row = sessions[args.mark_reviewed]
        if args.queued_at is not None and row.get("queued_at") != args.queued_at:
            print("session checkpoint changed; review its new evidence first", file=sys.stderr)
            return 2
        if not row.get("reviewed_at"):
            mark_reviewed(path, row)
    pending = [row for _, row in sessions.values() if not row.get("reviewed_at")]
    print("queued: %d, reviewed: %d, pending: %d" % (
        len(sessions), len(sessions) - len(pending), len(pending)))
    for row in pending:
        transcript = row.get("transcript_path")
        available = isinstance(transcript, str) and Path(transcript).is_file()
        print("%s  %s  transcript=%s" % (
            row["session_id"], row.get("queued_at", "unknown"), "available" if available else "missing"
        ))
    return 0


if __name__ == "__main__":
    sys.exit(main())
