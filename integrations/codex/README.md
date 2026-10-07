# Codex hooks for context-skills

## Install in a project

* Copy the `.codex` directory from `integrations/codex/` into the target project.
* Merge with existing configuration without overwriting unrelated hooks.
* When upgrading, replace references to `context_queue_session.py` with `context_register_session.py`.
* Add `.context/sessions/` to the project's `.gitignore`.
* Use `/hooks` in Codex to review and trust the project definitions.
* See the [official hook documentation](https://learn.chatgpt.com/docs/hooks) for the host contract.

```text
.codex/
  hooks.json
  hooks/
    context_register_session.py
```

* Require Git and Python 3 on `PATH`.
* Use `python3` on Linux/macOS; Windows commands use PowerShell and `python`.
* Commands resolve the Git root even from subdirectories with spaces.
* The registration hook exits quietly outside a Git checkout.

## Hook responsibilities

| Hook | Action |
| --- | --- |
| `SessionStart` | Explain apply, gather, import sessions, and the required context index. |
| `Stop`, `Interrupt`, `PreCompact`, `SessionEnd` | Register a session checkpoint through `context_register_session.py`. |

* Registration runs synchronously with a three-second timeout.
* It does not open transcripts, create the knowledge index, or invoke skills.
* Gather creates the index when processing knowledge.
* Import sessions reads selected transcripts and invokes gather.
* Hooks do not schedule imports or return continuation or blocking decisions.

## Session records

* Store records in `.context/sessions/` for the current Git worktree.
* Exclude this directory from knowledge retrieval, index rows, and article frontmatter rules.
* Keep exactly these four fields:

```json
{
  "session_id": "example-session-id",
  "updated_at": "2026-10-03T12:00:00+00:00",
  "transcript_path": "C:/sessions/example-session.jsonl",
  "reviewed_at": null
}
```

* Identify sessions by `session_id`, never by filename.
* New files use names such as `session-000001.json`; renamed records retain their identity.
* Each registration advances `updated_at` and resets `reviewed_at` to null.
* `transcript_path` is absolute when supplied; otherwise it is null.
* Do not store transcript text or message content in these records.

## Import selected checkpoints

* Use `context-import-sessions` with `context-gather` installed.
* Inventory records through the helper shipped with the import skill:

```text
python /path/to/context-import-sessions/scripts/context_read_sessions.py /path/to/project
```

* Retain the selected checkpoint's `updated_at` and read its transcript.
* Invoke gather with the loaded material and source locations.
* Mark the checkpoint only after gather completes successfully:

```text
python /path/to/context-import-sessions/scripts/context_read_sessions.py /path/to/project --mark-reviewed SESSION_ID --updated-at CHECKPOINT_TIMESTAMP
```

* Both options are required together.
* Leave missing evidence, incomplete processing, and report-only imports pending.
* A completed gather pass with no durable findings may still mark the checkpoint.
* A changed checkpoint remains pending; inspect new evidence before retrying.
* Repeating a mark for the same checkpoint is harmless.

## Storage guarantees

* Registration and import bookkeeping share an OS-backed `.queue.lock`.
* JSON updates replace files through temporary files.
* The lock prevents an old import from overwriting a newly registered checkpoint.
* A busy queue returns an error after a bounded wait.
* Malformed records and duplicate session IDs return errors instead of overwriting ambiguous state.
* The lock file remains after process exit; do not delete it while helpers are running.
* Each worktree owns its local queue; abrupt termination can prevent the final registration.
