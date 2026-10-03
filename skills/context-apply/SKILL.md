---
name: context-apply
description: Apply relevant project knowledge from .context to the current action, plan, or validation. Use for a known entry, an obvious match, resumed work, or a changed constraint. For discovering missing or conflicting sources, use context-gather.
---

# Apply Context

Connect relevant knowledge to observable behavior in the current task. Reading or citing an entry alone does not establish that the result follows it.

## Use only what the action needs

1. Read the known entry or obvious match through the project's navigation. Reuse sources already read when still applicable. An index and a prior gather step are optional; exclude `.context/sessions/` from knowledge retrieval.
2. Check scope and status. Every entry has `description` and `status` (`active`, `deprecated`, or `superseded`) in YAML frontmatter. Optional `related` lists entry-relative paths. A superseded entry requires an entry-relative `superseded_by` path: follow it to current knowledge, stopping at a broken link or cycle. Deprecated entries are withdrawn. Active does not turn a hypothesis into a fact.
3. Check consequential premises against current evidence when they may have changed. Code describes implementation, not necessarily accepted intent. Resolve conflicts from their authority and scope rather than silently choosing the easiest interpretation.
4. State the practical consequence where it matters: the behavior to preserve, the option ruled out, or the condition the next action must satisfy. Put it in the existing plan, change, or result; no separate application report is required.
5. Continue the authorized task. Tie meaningful validation to that consequence and distinguish planned checks from executed evidence.

For example, an adopted decision that an export preserves the snapshot at request acceptance means reopening it must preserve that snapshot. Requesting current data is a separate action. Merely mentioning the decision while changing reopening to use current records fails to apply it.

## Handle gaps without expanding the workflow

If information must be discovered, use `context-gather` when available or search the necessary sources directly. If the source does not contain an adopted choice, identify the unresolved decision; do not invent it. A check can resolve an empirical claim but cannot grant decision authority.

When CDE skills are present, pass the already-retrieved constraint or unresolved gap to the relevant investigation, decision, or validation workflow. Do not repeat retrieval or require every CDE step. Preserve previously granted authorization.

If no context affects the task, proceed without an artificial constraint. If work produces durable learning, consolidate it within scope, using `context-consolidate` when available. Describe actual impact and remaining limits; do not equate a declaration of use with proven compliance or a successful product outcome.
