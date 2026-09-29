#!/usr/bin/env python3
"""Inventory unreviewed session metadata from a project's local Git directory."""

import argparse
import datetime
import json
import os
import subprocess
import sys
from pathlib import Path


def queue_dir(project):
    result = subprocess.run(
        ["git", "-C", str(project), "rev-parse", "--git-common-dir"],
        check=True,
        capture_output=True,
        text=True,
    )
    path = Path(result.stdout.strip())
    if not path.is_absolute():
        path = (project / path).resolve()
    return path / "context-skills"


def read_rows(path):
    if not path.is_file():
        return []
    rows = []
    with path.open(encoding="utf-8") as handle:
        for number, line in enumerate(handle, 1):
            try:
                row = json.loads(line)
            except ValueError:
                print("skipped invalid JSON at %s:%d" % (path, number), file=sys.stderr)
                continue
            if isinstance(row, dict) and isinstance(row.get("session_id"), str):
                rows.append(row)
    return rows


def append_reviewed(path, session_id, queued_at):
    path.parent.mkdir(mode=0o700, exist_ok=True)
    record = {
        "session_id": session_id,
        "queued_at": queued_at,
        "reviewed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
    descriptor = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
    try:
        os.write(descriptor, (json.dumps(record) + "\n").encode("utf-8"))
    finally:
        os.close(descriptor)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", type=Path)
    parser.add_argument("--mark-reviewed", metavar="SESSION_ID")
    args = parser.parse_args()
    try:
        state = queue_dir(args.project_root.resolve())
    except (OSError, subprocess.SubprocessError):
        print("project_root is not an accessible Git checkout", file=sys.stderr)
        return 2
    queued = read_rows(state / "queue.jsonl")
    reviewed = {row["session_id"]: row.get("queued_at") for row in read_rows(state / "reviewed.jsonl")}
    by_id = {row["session_id"]: row for row in queued}
    if args.mark_reviewed:
        if args.mark_reviewed not in by_id:
            print("session is not in the queue", file=sys.stderr)
            return 2
        queued_at = by_id[args.mark_reviewed].get("queued_at")
        if args.mark_reviewed not in reviewed or reviewed[args.mark_reviewed] != queued_at:
            append_reviewed(state / "reviewed.jsonl", args.mark_reviewed, queued_at)
            reviewed[args.mark_reviewed] = queued_at
    pending = [row for session_id, row in by_id.items()
               if session_id not in reviewed or reviewed[session_id] != row.get("queued_at")]
    print("queued: %d, reviewed: %d, pending: %d" % (len(by_id), len(by_id) - len(pending), len(pending)))
    for row in pending:
        transcript = row.get("transcript_path")
        available = isinstance(transcript, str) and Path(transcript).is_file()
        print("%s  %s  transcript=%s" % (
            row["session_id"], row.get("queued_at", "unknown"), "available" if available else "missing"
        ))
    return 0


if __name__ == "__main__":
    sys.exit(main())
