#!/usr/bin/env python3
"""Give Codex a small retrieval reminder when the project has an index."""

import json
import subprocess
import sys
from pathlib import Path


def git_root(cwd):
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
    return Path(result.stdout.strip())


def main():
    try:
        event = json.loads(sys.stdin.read(65536))
    except (ValueError, OSError):
        return 0
    if not isinstance(event, dict) or event.get("hook_event_name") != "SessionStart":
        return 0
    cwd = event.get("cwd")
    if not isinstance(cwd, str) or not cwd:
        return 0
    root = git_root(Path(cwd))
    if root is None or not (root / ".context" / "INDEX.md").is_file():
        return 0
    output = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": (
                "This project has .context/INDEX.md. Read a known relevant "
                "entry directly; use context-find-related and a read-only subagent "
                "only for a broad or ambiguous search across many entries."
            ),
        }
    }
    print(json.dumps(output))
    return 0


if __name__ == "__main__":
    sys.exit(main())
