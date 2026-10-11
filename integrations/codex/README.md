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

* Registration runs synchronously. `Stop` and `PreCompact` have a five-second timeout;
  `Interrupt` and `SessionEnd` retain the host's three-second maximum.
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
* Each accepted registration advances `updated_at` and resets `reviewed_at` to null.
* `transcript_path` is absolute when supplied. An event without a path retains a
  previously known path; a new session without a path is skipped without creating
  a record or a queue directory. Empty, whitespace-only, and non-string paths
  count as absent.
* Existing legacy records with a null path remain unchanged until an event supplies
  a path. The hook does not delete them or mark them reviewed.
* A supplied path may point to a file that has not been saved yet; keep that
  checkpoint so the transcript can be imported after it appears.
* Do not store transcript text or message content in these records.

## Sessions without transcript paths

* The [hook contract](https://learn.chatgpt.com/docs/hooks) allows a null
  `transcript_path`. It does not document `turn_trigger` or a composer-prediction
  flag for the registration events. Missing paths alone do not establish the
  session's purpose.
* [Issue #3](https://github.com/LeszekKantorek/context-skills/issues/3) identified
  internal `composer_predictions` sessions through Codex logs. A read-only local
  check on 2026-10-11 independently found that marker for three of the five example
  IDs, and found no transcript files or durable thread entries for any of the five.
  The two other IDs had no matching logs in the database snapshot inspected.
  This check opened SQLite with `mode=ro&immutable=1`, excluding current WAL data;
  an absent match is not proof that the session never existed.
* Skipping a new pathless session prevents unusable queue entries without guessing
  whether it is a prediction, a normal session, or a subagent. An event that later
  supplies a path registers the session normally. A session whose events never
  supply a path will require explicit discovery before it can be imported.
* For a legacy `missing-path` record, first look for the exact session ID in the
  user's Codex session and archived-session filenames. If found, verify the ID
  and project identity in the selected transcript before importing it explicitly.
  Do not substitute a transcript merely because its timestamp or directory matches.
* The local Codex thread index may provide `rollout_path`; logs may associate an ID
  with `composer_predictions`. These are diagnostic leads, not stable hook APIs.
  Missing log entries or `has_user_event=0` alone do not justify deleting a record
  or excluding subagents. Confirmed prediction records can be removed during an
  explicitly requested cleanup; unresolved records stay pending.
* The hook does not scan session directories or query private SQLite databases.
  Such discovery would add latency and dependencies on host-specific storage to
  every registration, and cannot recover a transcript that was never saved.

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
* Listing reports `available`, `missing-path`, and `missing-file` separately and
  reads queue JSON only; it does not read transcript contents or create a lock.
* A listing is an inventory of individual atomic records, not a locked snapshot
  of the whole queue. Always retain and check the selected `updated_at` on review.
* Leave missing evidence, incomplete processing, and report-only imports pending.
* A completed gather pass with no durable findings may still mark the checkpoint.
* A changed checkpoint remains pending; inspect new evidence before retrying.
* Repeating a mark for the same checkpoint is harmless.

## Storage guarantees

* Registration and review bookkeeping share an OS-backed `.queue.lock`; inventory
  listing does not acquire it or write to the queue.
* JSON updates replace files through temporary files.
* Both writers retry replacement for Windows errors 5, 32, and 33 for up to one
  second, with 20 ms between attempts. Other errors fail immediately. Failed
  replacement retains the previous record and cleans up the temporary file.
* Git discovery, lock acquisition, and replacement each have a one-second bound.
  The three-second host limit on `Interrupt` and `SessionEnd` also includes process
  startup, so a final checkpoint can still be lost under sustained contention.
* The lock prevents an old import from overwriting a newly registered checkpoint.
* A busy queue returns an error after a bounded wait.
* Malformed records and duplicate session IDs return errors instead of overwriting ambiguous state.
* The lock file remains after process exit; do not delete it while helpers are running.
* Each worktree owns its local queue; abrupt termination can prevent the final registration.
