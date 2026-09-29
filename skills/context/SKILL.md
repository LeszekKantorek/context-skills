---
name: context
description: Retrieve and maintain selective project memory in .context. Use at task start to find relevant knowledge, after a meaningful task or decision to consolidate durable learning, or when asked to initialize project memory. Do not use as a transcript or active task tracker.
---

# Context

Keep project memory small enough to retrieve and specific enough to change a future decision or action. `.context/INDEX.md` is the only required retrieval path; the project chooses all other entry files and folders.

## Start work

1. When project memory may help, read a known entry directly or use the short `.context/INDEX.md` to select an obvious match. Use `context-find-related` for a broad or ambiguous search across many entries; delegate that search to one read-only subagent when available. Do not spawn an agent for a known file or a quick index lookup. Treat `observed` as a lead requiring verification and do not use `superseded` entries as current guidance.
2. Verify a critical claim against current code, tests, or an authoritative source when it may have changed. Treat an entry as a lead, not stronger evidence than the source it describes.
3. If the index is absent, continue the task. Initialize `.context/` only when the user requests memory or the work yields a clear first durable entry. Do not create an empty taxonomy.

## Consolidate at a meaningful boundary

Use a completed task, experiment, incident, or decision as the trigger. Review what was learned and compare each candidate with existing entries.

Keep a candidate only when it is project-specific, likely to remain useful, supported by evidence or clearly marked `observed`, not duplicated, and has a precise answer to “when should I read this?” A single ambiguous sighting can remain in the task's notes; no memory change is a valid result. See [entry contract](references/entry-contract.md) for the simple index and entry frontmatter.

Store a useful but unconfirmed observation as an ordinary indexed entry with `status: observed`. Record its evidence and uncertainty in the body. Promote it to `active` when confirmed; do not maintain separate observation or change ledgers.

Choose the kind of information that best serves a future reader. These are writing prompts, not tags, frontmatter fields, or required directories:

| Future question | Useful content |
| --- | --- |
| What is true here? | Fact or model: scope, source, uncertainty, staleness conditions. |
| What must remain true? | Constraint or invariant: boundary, consequence, validation. |
| How do we do this? | Procedure: preconditions, steps, checks, stop conditions. |
| What happened? | Experience or incident: situation, outcome, evidence, useful follow-up. |
| What did we learn? | Lesson or pattern: observation, cause, changed behavior, limits. |
| Why was this chosen? | Decision: options, rationale, consequences, reopen condition. |
| What local practice applies? | Convention: trigger, action, source of authority. |
| What preference persists? | Preference: whose, scope, evidence, when to reconfirm. |

One event can inform several entries, but create only those that would help future work. Current task progress belongs in the task's own issue or plan, not project memory.

Update the existing entry when it already owns the topic. Otherwise create one focused file in a path that fits the project's current organization. Keep its index `Use when…` instruction accurate and its frontmatter `description` and `status` current. Do not create a folder merely to represent a type or hold one file.

## Boundaries

- Keep current goals, progress, ownership, blockers, and next steps in the issue, plan, task file, branch, or worktree that owns them.
- Never commit transcripts, generated logs, secrets, credentials, or personal message text to `.context/`.
- Add or update a clearly scoped entry when the task authorizes project memory changes. Propose changes to accepted decisions with contested evidence, user-authored instructions, hook settings, permissions, or large reorganizations.
- When new evidence contradicts memory, verify it and mark the old claim superseded or propose a resolution. Do not leave two active incompatible claims.
- If this project also uses a journal or another memory system, link to its canonical lesson rather than copying it.

Report what was retrieved, written, updated, proposed, or deliberately skipped, with a short evidence pointer. Do not imply that an entry was used or verified without evidence.

## Companions

- `context-find-related` delegates broad memory searches while leaving simple reads with the main agent.
- `context-harvest` reviews completed sessions across tasks.
- `context-feedback` checks whether prior entries help in practice.
- `context-maintenance` reconciles accumulated memory and its index.
