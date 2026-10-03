# Codex hooks for context-skills

These optional project hooks implement a cheap start reminder and frequent metadata checkpoints. They do not create memory entries or invoke a model; run `context-harvest` separately to review the queued sessions.

## Install in a project

Copy the entire `.codex` directory from `integrations/codex/` to the target project's root. Its contents already have the required names and layout:

```text
.codex/
├── hooks.json
└── hooks/
    └── context_queue_session.py
```

If the project already has a `.codex` directory, merge its contents. Review and merge an existing `.codex/hooks.json`; do not overwrite other hooks. If upgrading the previous SessionEnd-only configuration, replace its handler rather than adding a second SessionEnd handler. The session metadata commands resolve the project Git root, so they work when Codex starts from a subdirectory. When upgrading, remove the unused `.codex/hooks/context_session_start.py` script.

The hooks require Git and Python 3 on `PATH`: `python3` on Linux/macOS, or `python` on Windows. Windows metadata commands use `commandWindows` and explicitly invoke PowerShell to resolve the Git root, including paths containing spaces. `SessionStart` uses only the shell built-in `echo`.

Use `/hooks` in Codex to review and trust the exact project hook definitions. [Official Codex hook documentation](https://learn.chatgpt.com/docs/hooks) describes trust, event timing, and output contracts. Hook settings are project configuration; installation should be a deliberate project choice.

`SessionStart` runs `echo` directly from `hooks.json` to remind the agent to use `context` for relevant project memory and durable, evidence-backed learning. The reminder runs even if `.context/INDEX.md` does not exist yet. Plain text output from this event is added to the agent context; no helper script is needed. It does not launch a subagent or require a memory read for every task. The main agent can read a known entry directly; `context-find-related` delegates only broad or ambiguous searches when the host supports it. A shared script updates session metadata on `Stop` (turn completion), `Interrupt` (user interruption), `PreCompact` (before compaction), and `SessionEnd` (session closure). Each handler has a three-second timeout and runs synchronously so a background write is not cancelled at session exit. The script returns no continuation or blocking decisions.

The record includes `session_id`, `transcript_path`, `cwd`, repository root, timestamp, event name, and optional turn ID. Each session has one file at `.context/sessions/<session-id>.json` in the current worktree. The same file stores `reviewed_at`: `null` while pending, or a timestamp after review. No transcript is opened, and no transcript or assistant message content is stored. Add `.context/sessions/` to the target project's `.gitignore` so session metadata stays outside tracked files. Each worktree has its own session directory.

Each event replaces the session file with its latest checkpoint and resets `reviewed_at` to `null`. `scan_queue.py` lists each session once and marks review in that same file; there is no separate review ledger. A new checkpoint after a review makes the session pending again. These checkpoints can refer to an active session: harvest should review a stable snapshot or wait until the session is idle before marking it reviewed. Hook registration does not schedule harvest. Abrupt process termination can still prevent a hook from running.

If a project is not a Git checkout, the hooks exit quietly. The skills themselves still work with a supplied `.context/` or transcript path.
