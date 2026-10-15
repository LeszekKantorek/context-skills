# Codex hooks for context-skills

## Install in a project

* Copy the `.codex` directory from `integrations/codex/` into the target project.
* Merge with existing configuration without overwriting unrelated hooks.
* When upgrading, replace references to `context_queue_session.py` with `context_register_session.py`.
* Add `.context/sessions.log` and `.context/.sessions.lock` to the project's `.gitignore`.
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
| `Stop`, `Interrupt`, `PreCompact`, `SessionEnd` | Register a session through `context_register_session.py`. |

* Registration runs synchronously. `Stop` and `PreCompact` have a five-second timeout;
  `Interrupt` and `SessionEnd` retain the host's three-second maximum.
* It does not open transcripts, create the knowledge index, or invoke skills.
* Gather creates the index when processing knowledge.
* Import sessions reads selected transcripts and invokes gather.
* Hooks do not schedule imports or return continuation or blocking decisions.

## Session records

* Store one row per session in `.context/sessions.log`, encoded as UTF-8 CSV.
* The first line contains exactly these four column names:

```csv
session_date,session_id,path,reviewed_date
2026-10-14,example-session-id,C:/sessions/example-session.jsonl,
```

* Dates use `YYYY-MM-DD` in the machine's local timezone.
* `session_date` records the first registration date and remains unchanged on later events.
* `session_id` contains the session ID. Row order does not establish identity.
* `path` contains the absolute transcript path.
* An empty `reviewed_date` means pending. A completed review sets today's date.
* Repeated registration of an existing `session_id` preserves its `reviewed_date`.
* CSV quoting preserves commas, quotes, and Unicode in paths and IDs.
* The log contains metadata only. Exclude it and its lock file from project knowledge.
* An event without a nonempty transcript path creates no row or context directory and does not change existing rows.
* Empty, whitespace-only, and non-string paths count as absent.
* A supplied path may precede the transcript file. New sessions start with an empty review date.

* Only the current CSV schema is supported. There is no migration or fallback reader.
* Existing session IDs update the same row without creating duplicates, even during concurrent registration.

## Review pending sessions

* Use `context-review-sessions` with `context-preserve` installed.
* List pending sessions through the bundled helper:

```text
python /path/to/context-review-sessions/scripts/context_read_sessions.py /path/to/project
```

* Use the file sizes and availability to choose sessions and delegate preservation as needed.
* Mark fully reviewed sessions after context-preserve finishes successfully:

```text
python /path/to/context-review-sessions/scripts/context_read_sessions.py /path/to/project --mark-reviewed SESSION_ID [SESSION_ID ...]
```

* Listing reports `available`, `missing-file`, or `unavailable`. An empty path in the log is invalid.
* It reads one log snapshot and transcript metadata, without reading transcript contents or creating a lock.
* Marking checks all supplied IDs and transcript availability before saving the registry once.
* Unknown IDs or unavailable transcripts prevent the entire update.
* Leave missing evidence, incomplete processing, and report-only reviews pending.
* A completed preservation pass with no new findings can still mark the sessions as reviewed.
* Repeating a mark preserves existing review dates.

## Storage guarantees

* Registration and review bookkeeping share an OS-backed `.context/.sessions.lock`.
* Both writers read the current log under the lock and atomically replace the entire log through a temporary file.
* Inventory listing reads the log without acquiring the writer lock.
* After any I/O error while creating, writing, closing, or replacing the temporary file, the writer retries the full write once.
* The retry waits 50 ms and runs under the same lock. A second failure returns an error and preserves the previous log.
* Temporary files are removed after each attempt. Invalid data fails before writing and is not retried.
* Git discovery and lock acquisition each have a one-second bound. Hook timeouts still apply to the complete process.
* The lock prevents writers from discarding each other's rows or review dates.
* Review validation compares the retained token with the current record and transcript metadata under the lock.
* A busy queue returns an error after a bounded wait.
* Malformed CSV, invalid dates, and duplicate session IDs return errors instead of overwriting ambiguous state.
* The lock file remains after process exit; do not delete it while helpers are running.
* Each worktree owns its local queue; abrupt termination can prevent the final registration.
