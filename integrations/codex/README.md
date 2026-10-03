# Codex hooks for context-skills

The optional integration keeps a short context reminder and a local queue of session checkpoints. Registration stores metadata only; context-consolidate performs the actual session review when requested.

## Install in a project

Copy the `.codex` directory from `integrations/codex/` into the target project's root:

```text
.codex/
├── hooks.json
└── hooks/
    └── context_queue_session.py
```

Merge with existing project configuration without overwriting unrelated hooks. Add `.context/sessions/` to the target project's `.gitignore`. Use `/hooks` in Codex to review and trust the project definitions. See the [official hook documentation](https://learn.chatgpt.com/docs/hooks) for the host's input and output contract.

The registration hooks require Git and Python 3 on `PATH`: `python3` on Linux/macOS or `python` on Windows. Windows commands use `commandWindows` with PowerShell. Commands resolve the repository root, including when work starts in a subdirectory containing spaces. The hook exits quietly outside a Git checkout; the skills can still work with explicitly supplied context and sessions.

## What runs

`SessionStart` uses `echo` to remind the agent to apply relevant context, gather missing sources, and consolidate durable learning. It does not require an index or a full memory read.

`Stop`, `Interrupt`, `PreCompact`, and `SessionEnd` run the registration script synchronously with a three-second timeout. They do not open transcripts or create knowledge entries. The script returns no continuation or blocking decisions.

## Session records

The queue lives in `.context/sessions/` for the current worktree. It is technical state, excluded from knowledge retrieval and entry frontmatter rules. Each record has exactly four fields:

```json
{
  "session_id": "example-session-id",
  "updated_at": "2026-10-03T12:00:00+00:00",
  "transcript_path": "C:/sessions/example-session.jsonl",
  "reviewed_at": null
}
```

`session_id` identifies the session. It is never inferred from the filename. New records use names such as `session-000001.json`; registration also finds and updates an existing renamed record by its JSON identity.

`updated_at` identifies the latest registered checkpoint. Each new event updates it and resets `reviewed_at` to null. `transcript_path` is an absolute path when supplied, otherwise null. No transcript content, message text, event name, turn ID, or project-directory metadata is stored in the record.

Both the registration hook and review helper use the same OS-backed `.queue.lock` and replace JSON records through temporary files. The lock makes checking a checkpoint and marking it reviewed one operation relative to registration. It is automatically released on process exit; the small lock file remains and should not be deleted while helpers are running. A busy queue produces an explicit error after a bounded wait.

Malformed records and duplicate `session_id` values produce an error rather than silently choosing a record or overwriting ambiguous state. The four-field record format is the only supported format.

## Review selected checkpoints

Run the helper shipped with context-consolidate, using its installed path:

```text
python /path/to/context-consolidate/scripts/scan_queue.py /path/to/project
```

The inventory shows each pending session's identity, checkpoint, transcript availability, and record path. It does not analyze session content. Inspect selected project-relevant sessions, retain their `updated_at` values, and consolidate useful evidence.

After actually reviewing a checkpoint:

```text
python /path/to/context-consolidate/scripts/scan_queue.py /path/to/project --mark-reviewed SESSION_ID --updated-at CHECKPOINT_TIMESTAMP
```

Both options are required together. If a newer event was registered, the helper refuses to mark the old checkpoint as reviewed. Do not substitute the newer timestamp without inspecting its evidence. Repeating a mark for the same checkpoint is harmless.

Checkpoints can belong to active sessions. Review an idle session or a stable snapshot; a missing transcript is missing evidence, not a completed review. Each worktree owns its local queue. Registration does not schedule a review, and abrupt termination can prevent the final hook from running.
