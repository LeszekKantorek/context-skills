---
name: context-harvest
description: Review completed agent sessions for durable project knowledge missing from .context. Use after several related tasks, on a schedule, or when important discoveries were not recorded during work. For task-start retrieval or one completed task, use context.
---

# Context Harvest

Inspect completed work as evidence for project memory. Accept explicit transcript paths, a set of session identifiers, or a local queue produced by optional lifecycle hooks. Do not assume a particular agent product or transcript format. Queue entries may be checkpoints from active sessions; select idle sessions or a stable snapshot and do not mark unseen later work as reviewed.

## Review

1. Establish the target project and bounded set of sessions. If a queue exists, run `python3 scripts/scan_queue.py <project-root>` to inventory queued items and detect missing transcripts. Resolve `scripts/` relative to this skill. The scan is metadata only.
2. Inspect only sessions relevant to this project. Worktrees may have different working directories, so verify repository identity instead of matching a directory string alone. Use commits, diffs, issues, test results, and current source as stronger evidence when available.
3. Extract candidate facts, procedures, incidents, lessons, decisions, constraints, and preferences. Record the source session and approximate turn or time, the claim, and confidence. Distinguish agent assertions from user decisions and verified source behavior.
4. Compare candidates with `.context/INDEX.md` and relevant entries. Retain a candidate only if it is project-specific, likely to remain useful, has evidence, is non-duplicate, and could change a future decision or action. Give its index link a precise `Use when…` instruction (at most two sentences); give the entry `description` (at most four sentences) and `status` frontmatter. Use `observed` for a useful but unconfirmed pattern and `active` only when supported. Put evidence, scope, or uncertainty in the body as needed. Keep the project's existing paths; information types never require matching subfolders. Leave ambiguous candidates without clear future use as questions in the report.
5. Prepare a reviewable entry and index change. Mark a session processed in local queue state only after its evidence was actually reviewed. A run with no durable learning makes no `.context/` change.

Use the local helper for queue bookkeeping:

```bash
python3 scripts/scan_queue.py <project-root>
python3 scripts/scan_queue.py <project-root> --mark-reviewed <session-id>
```

The inventory shows identifiers and transcript availability. Read the corresponding metadata records in `<git-common-dir>/context-skills/queue.jsonl` to locate the selected sources; obtain the common directory with `git rev-parse --git-common-dir`. The second command records the queued revision reviewed; it does not read or delete a transcript. If a resumed session is queued again, review its new evidence on a later pass.

## Boundaries and report

Never send session content to an external search service. Do not copy raw transcripts, secrets, personal conversation, or tool logs into project memory. If a source is inaccessible, say which evidence is missing and continue with independent evidence.

Report the number of sessions inspected, candidates kept and rejected, evidence for retained entries, files changed or proposed, and any inaccessible sources. Do not claim that scanning metadata verified a memory candidate.
