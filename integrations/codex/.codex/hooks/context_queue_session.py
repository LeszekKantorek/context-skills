#!/usr/bin/env python3
"""Queue metadata for later context review without reading the transcript."""

import datetime
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

QUEUE_EVENTS = {"Stop", "Interrupt", "PreCompact", "SessionEnd"}


def git_paths(cwd):
    try:
        result = subprocess.run(
            ["git", "-C", str(cwd), "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
            timeout=1,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    lines = result.stdout.splitlines()
    if len(lines) != 1:
        return None
    root = Path(lines[0]).resolve()
    return root


def main():
    try:
        event = json.load(sys.stdin)
    except (ValueError, OSError):
        return 0
    if not isinstance(event, dict) or event.get("hook_event_name") not in QUEUE_EVENTS:
        return 0
    session_id = event.get("session_id")
    cwd_value = event.get("cwd")
    if (not isinstance(session_id, str)
            or not re.fullmatch(r"[A-Za-z0-9_-]{1,128}", session_id)
            or re.fullmatch(r"(?i:CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])", session_id)):
        return 0
    if not isinstance(cwd_value, str) or not cwd_value:
        return 0
    cwd = Path(cwd_value).resolve()
    paths = git_paths(cwd)
    if paths is None:
        return 0
    root = paths
    transcript = event.get("transcript_path")
    if not isinstance(transcript, str):
        transcript = None
    item = {
        "session_id": session_id,
        "hook_event_name": event["hook_event_name"],
        "turn_id": event.get("turn_id") if isinstance(event.get("turn_id"), str) else None,
        "transcript_path": transcript,
        "cwd": str(cwd),
        "repo_root": str(root),
        "queued_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "reviewed_at": None,
    }
    queue_dir = root / ".context" / "sessions"
    temporary_path = None
    try:
        queue_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
        queue_path = queue_dir / (session_id + ".json")
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=queue_dir,
                                         suffix=".tmp", delete=False) as handle:
            temporary_path = Path(handle.name)
            json.dump(item, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(temporary_path, queue_path)
    except OSError as exc:
        print("context-skills: could not queue session: %s" % exc, file=sys.stderr)
        return 1
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
    if event["hook_event_name"] in {"Stop", "PreCompact"}:
        print("{}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
