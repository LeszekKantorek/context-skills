# Codex hooks for context-skills

These optional project hooks implement a cheap start reminder and frequent metadata checkpoints. They do not create memory entries or invoke a model; run `context-harvest` separately to review the queued sessions.

## Install in a project

Copy `hooks.json` to the target project's `.codex/hooks.json`, `session_start.py` to `.codex/hooks/context_session_start.py`, and `queue_session.py` to `.codex/hooks/context_queue_session.py`. Review and merge an existing `.codex/hooks.json`; do not overwrite other hooks. If upgrading the previous SessionEnd-only configuration, replace its handler rather than adding a second SessionEnd handler. The commands resolve the project Git root, so they work when Codex starts from a subdirectory.

Use `/hooks` in Codex to review and trust the exact project hook definitions. [Official Codex hook documentation](https://learn.chatgpt.com/docs/hooks) describes trust, event timing, and output contracts. Hook settings are project configuration; installation should be a deliberate project choice.

`SessionStart` emits a short reminder only when `.context/INDEX.md` exists. It does not launch a subagent or require a memory read for every task. The main agent can read a known entry directly; `context-find-related` delegates only broad or ambiguous searches when the host supports it. A shared script appends metadata on `Stop` (turn completion), `Interrupt` (user interruption), `PreCompact` (before compaction), and `SessionEnd` (session closure). Each handler has a three-second timeout and runs synchronously so a background write is not cancelled at session exit. The script returns no continuation or blocking decisions.

The record includes `session_id`, `transcript_path`, `cwd`, repository root, timestamp, event name, and optional turn ID. Records live in the local Git common directory at `context-skills/queue.jsonl`. No transcript is opened, and no transcript or assistant message content is stored. The queue stays outside tracked files, including in projects with multiple worktrees.

Multiple events append multiple checkpoints. `scan_queue.py` selects the latest checkpoint per session and lists that session once. A new checkpoint after a review makes the session pending again. These checkpoints can refer to an active session: harvest should review a stable snapshot or wait until the session is idle before marking it reviewed. Hook registration does not schedule harvest. Abrupt process termination can still prevent a hook from running.

If a project is not a Git checkout, the hooks exit quietly. The skills themselves still work with a supplied `.context/` or transcript path.
