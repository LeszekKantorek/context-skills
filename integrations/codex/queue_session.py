#!/usr/bin/env python3
"""Queue metadata for later context review without reading the transcript."""

import datetime
import json
import os
import subprocess
import sys
from pathlib import Path

QUEUE_EVENTS = {"Stop", "Interrupt", "PreCompact", "SessionEnd"}


def git_paths(cwd):
    try:
        result = subprocess.run(
            ["git", "-C", str(cwd), "rev-parse", "--show-toplevel", "--git-common-dir"],
            check=True,
            capture_output=True,
            text=True,
            timeout=1,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    lines = result.stdout.splitlines()
    if len(lines) != 2:
        return None
    root = Path(lines[0]).resolve()
    common = Path(lines[1])
    if not common.is_absolute():
        common = (cwd / common).resolve()
    return root, common


def main():
    try:
        event = json.load(sys.stdin)
    except (ValueError, OSError):
        return 0
    if not isinstance(event, dict) or event.get("hook_event_name") not in QUEUE_EVENTS:
        return 0
    session_id = event.get("session_id")
    cwd_value = event.get("cwd")
    if not isinstance(session_id, str) or not 0 < len(session_id) <= 256:
        return 0
    if not isinstance(cwd_value, str) or not cwd_value:
        return 0
    cwd = Path(cwd_value).resolve()
    paths = git_paths(cwd)
    if paths is None:
        return 0
    root, common = paths
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
    }
    queue_dir = common / "context-skills"
    try:
        queue_dir.mkdir(mode=0o700, exist_ok=True)
        queue_path = queue_dir / "queue.jsonl"
        descriptor = os.open(queue_path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
        try:
            os.write(descriptor, (json.dumps(item, ensure_ascii=False) + "\n").encode("utf-8"))
        finally:
            os.close(descriptor)
    except OSError as exc:
        print("context-skills: could not queue session: %s" % exc, file=sys.stderr)
        return 1
    if event["hook_event_name"] in {"Stop", "PreCompact"}:
        print("{}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
