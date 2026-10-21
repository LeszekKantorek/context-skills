# Codex hooks for context-skills

## Install in a project

* Copy the `.codex` directory from `integrations/codex/` into the target project.
* Merge with existing configuration without overwriting unrelated hooks.
* Add `.context/sessions.log` to the project's `.gitignore`.
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
| `SessionStart` | Summarize the six context skills and register the session when its transcript path is available. |
| `Stop`, `Interrupt`, `PreCompact`, `SessionEnd` | Register the session when its transcript path is available. |

* Registration runs synchronously. `Stop` and `PreCompact` have a five-second timeout;
  `Interrupt` and `SessionEnd` retain the host's three-second maximum.
* Registration stores session metadata without opening transcripts or invoking skills.
* The startup reminder covers `context-preserve`, `context-review-sessions`, `context-map`, `context-maintain`, `context-diagnose`, and `context-compile`.
* Skills work with existing project documents; no index format or skill sequence is required.
* `context-review-sessions` coordinates pending reviews through `context-preserve`.
* Hooks do not schedule reviews or return continuation or blocking decisions.

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
* Repeated registration of an existing `session_id` leaves its row unchanged.
* CSV quoting preserves commas, quotes, and Unicode in paths and IDs.
* The log contains metadata only. Exclude it from project knowledge.
* An event without a nonempty transcript path creates no row or context directory.
* Empty, whitespace-only, and non-string paths count as absent.
* A supplied path may precede the transcript file. New sessions start with an empty review date.

* Only the current CSV schema is supported. There is no migration or fallback reader.
* Existing session IDs are skipped. A failed registration write is retried once after 500 ms.

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
* It reads one log snapshot and transcript metadata, without reading transcript contents or creating a lock file.
* Marking checks all supplied IDs and transcript availability before saving the registry once.
* Unknown IDs or unavailable transcripts prevent the entire update.
* Leave missing evidence, incomplete processing, and report-only reviews pending.
* A completed preservation pass with no new findings can still mark the sessions as reviewed.
* Repeating a mark preserves existing review dates.

## Storage behavior

* The hook appends to `.context/sessions.log` without a separate lock file.
* If registration fails, it retries once after 500 ms. A second failure returns an error.
* Review bookkeeping rewrites the session log directly; do not run a review update at the same time as registration.
* Each worktree owns its local queue; abrupt termination can prevent the final registration.
