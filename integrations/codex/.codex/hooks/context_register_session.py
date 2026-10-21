#!/usr/bin/env python3
"""Register a session transcript for later review."""

import csv
import datetime
import json
import subprocess
import sys
import time
from pathlib import Path

FIELDS = ("session_date", "session_id", "path", "reviewed_date")
REGISTER_EVENTS = {"SessionStart", "Stop", "Interrupt", "PreCompact", "SessionEnd"}


def register(directory, session_id, transcript_path):
    if not isinstance(transcript_path, str) or not transcript_path.strip():
        return

    log = directory / "sessions.log"
    for attempt in range(2):
        try:
            directory.mkdir(parents=True, exist_ok=True)
            needs_header = not log.exists() or log.stat().st_size == 0
            if log.exists():
                with log.open(encoding="utf-8", newline="") as handle:
                    rows = list(csv.DictReader(handle))
                if any(row.get("session_id") == session_id for row in rows):
                    return
            else:
                rows = []

            with log.open("a", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
                if needs_header:
                    writer.writeheader()
                writer.writerow({
                    "session_date": datetime.date.today().isoformat(),
                    "session_id": session_id,
                    "path": transcript_path,
                    "reviewed_date": "",
                })
            return
        except OSError:
            if attempt:
                raise
            time.sleep(0.5)


def main():
    try:
        event = json.load(sys.stdin)
    except (ValueError, OSError):
        return 0
    if not isinstance(event, dict) or event.get("hook_event_name") not in REGISTER_EVENTS:
        return 0

    session_id, cwd = event.get("session_id"), event.get("cwd")
    transcript = event.get("transcript_path")
    if (not isinstance(session_id, str) or not session_id
            or not isinstance(cwd, str) or not cwd
            or not isinstance(transcript, str) or not transcript.strip()):
        return 0

    try:
        root = subprocess.run(
            ["git", "-C", cwd, "rev-parse", "--show-toplevel"],
            check=True, capture_output=True, text=True, timeout=1,
        ).stdout.strip()
        path = str((Path(cwd) / transcript).resolve())
        register(Path(root) / ".context", session_id, path)
    except (OSError, subprocess.SubprocessError, ValueError, csv.Error) as exc:
        print("context-skills: could not register session: %s" % exc, file=sys.stderr)
        return 1

    if event["hook_event_name"] in {"Stop", "PreCompact"}:
        print("{}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
