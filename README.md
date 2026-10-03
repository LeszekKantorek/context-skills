# context-skills

Project memory that agents can retrieve selectively and keep useful over time.

The skill family follows a simple loop: capture evidence, decide whether it is durable, write the smallest useful memory, check whether it helped, and maintain the collection. It focuses on project knowledge.

## Skills

| Skill | Use it for |
| --- | --- |
| [`context`](skills/context/SKILL.md) | Consolidate durable project knowledge and retrieve relevant entries. |
| [`context-find-related`](skills/context-find-related/SKILL.md) | Find related project-memory entries through a broad search delegated to a small read-only subagent. |
| [`context-harvest`](skills/context-harvest/SKILL.md) | Review completed sessions together for durable knowledge that was missed during work. |
| [`context-feedback`](skills/context-feedback/SKILL.md) | Check whether entries were retrieved and helped, using direct, inferred, or unknown usage evidence. |
| [`context-maintenance`](skills/context-maintenance/SKILL.md) | Resolve duplicate, stale, contradictory, and oversized memory. |

Install all five skills with `npx skills add LeszekKantorek/context-skills`, or select one with `npx skills add LeszekKantorek/context-skills@context-find-related` (likewise for the other names). Install `context` and `context-find-related` together for broad-search delegation.

## Memory belongs to the project

The only fixed retrieval file is `.context/INDEX.md`. Each line contains a link (with the entry title) and a specific `Use when…` instruction of at most two sentences. No index tags, types, or status fields. Projects choose the remaining paths to match their own domains and navigation habits:

```text
.context/
├── INDEX.md
├── architecture/read-model.md
├── operations/local-release.md
└── product/freshness.md
```

An entry may describe a fact, model, constraint, procedure, experience, lesson, decision, convention, preference, or another useful type. The type guides what the entry should explain; it does not choose a directory. Empty category folders are never required.

Each entry starts with minimal YAML frontmatter: `description` (at most four sentences) and `status` (`observed`, `active`, or `superseded`). The index answers *when to open it*; the description answers *what is inside*. An `observed` entry is a useful but unconfirmed lead, not established guidance. Evidence and details belong in the entry body. Superseded entries can remain for history, but are not listed in the index. There are no separate `observations.md` or `changes.md` ledgers; Git records edits.

When the relevant entry is known, the main agent reads it directly. It can also scan a short index for an obvious match. `context-find-related` delegates only broad or ambiguous searches across many entries to one read-only subagent when the host supports delegation; the parent receives concise findings instead of the entire scan. Separate context can keep a large search out of the parent conversation, but does not guarantee fewer total tokens. At a meaningful boundary, compare new evidence with existing memory and write only what would change a future decision or action. Current goals, progress, ownership, and blockers stay in the task's issue or plan.

## Hooks

The optional [Codex hook configuration](integrations/codex/.codex/hooks.json) and scripts provide inexpensive retrieval and queue updates:

- `SessionStart` prints a short reminder to use `context` for relevant project memory and durable learning; it does not require a memory read when irrelevant.
- `Stop`, `Interrupt`, `PreCompact`, and `SessionEnd` update session metadata in `.context/sessions/<session-id>.json`. They do not read or commit transcripts, invoke a model, or create memory entries. Harvest lists the latest checkpoint once per session.

To enable these hooks in a project, copy the configuration and scripts as described in [hook setup](integrations/codex/README.md). Codex requires project hook trust review. The skills work without hooks; `context-harvest` can inspect sessions supplied explicitly.

## Safety and cadence

The agent may add a new, evidence-backed entry or update a clearly owned entry within the requested project. It proposes changes to conflicting accepted decisions, user-authored instruction files, hook settings, permissions, and broad reorganizations. It never stores secrets or raw conversation text in `.context/`.

Run `context-harvest` after a set of completed sessions, `context-feedback` periodically when there is usage evidence, and `context-maintenance` when the collection becomes stale or hard to navigate. An empty review is a valid result.

## Development checks

```bash
python3 -m unittest discover -s tests
python3 -m py_compile integrations/codex/.codex/hooks/*.py skills/context-harvest/scripts/*.py
```
