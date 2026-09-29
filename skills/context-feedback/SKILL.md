---
name: context-feedback
description: Check whether existing .context entries were retrieved when relevant and helped future work. Use periodically after enough sessions exist, when an entry seems ignored or misleading, or before pruning memory. For creating new entries use context.
---

# Context Feedback

Measure whether stored memory earns its reading and maintenance cost. Start with `.context/INDEX.md` and the available recent project sessions or task records. If there is no index or no usage evidence, report that limit rather than guessing.

For each entry in scope:

1. Confirm the file exists, its frontmatter `description` and `status` are accurate, and its index `Use when…` instruction still identifies the right tasks.
2. Find tasks where `Use when…` should have matched. Check whether the agent opened or cited the entry, whether the targeted mistake was avoided, and whether the entry was contradicted or caused friction.
3. Label usage evidence `direct`, `inferred`, or `unknown`. This label is separate from an entry's `observed` status. Absence of a rare task is not evidence that a rare but important decision is useless.
4. Grade the feedback as `verified`, `watching`, `needs-update`, or `prune-proposed`. These are report grades, not entry statuses. Record the reason and evidence pointer in the report. Promote `observed` to `active` only with confirmation; change other statuses only when supported by evidence. Propose removal of user-authored or consequential material.

Keep feedback compact. A useful report lists entries checked, matching tasks observed, grades, and specific changes. If all judgments are unknown, suggest the smallest evidence source that would help next time; do not manufacture usage counts or add automatic tracking without a demonstrated need.
