# context-skills

Apply project knowledge, gather durable learning, and import saved sessions into `.context/`.

## Choose a skill

| Need | Skill | Result |
| --- | --- | --- |
| Use stored knowledge in the current task | [context-apply](skills/context-apply/SKILL.md) | Read the index and relevant entries; reflect their rules in actions and checks. |
| Save session learning or review existing knowledge | [context-gather](skills/context-gather/SKILL.md) | Create, update, merge, or withdraw entries; create and maintain the index. |
| Process saved sessions or pending checkpoints | [context-import-sessions](skills/context-import-sessions/SKILL.md) | Load session material, invoke gather, and mark completed checkpoints. |

* `context-gather` combines the former `context-consolidate` and `context-review` responsibilities.
* Use `context-apply` during work and `context-gather` when knowledge should be saved or maintained.
* `context-import-sessions` handles session files; it requires `context-gather` for knowledge processing.
* No full skill sequence is required.

## Install

```text
npx skills add LeszekKantorek/context-skills
```

* Select a single skill with `npx skills add LeszekKantorek/context-skills@context-apply` or another name from the table.
* Install `context-gather` alongside `context-import-sessions`.
* When updating an existing installation, remove the retired `context-consolidate` and `context-review` skill copies.

## Context index

* **Gather creates `.context/INDEX.md` when no context index exists.** An existing index is updated in place.
* The index contains only a table with `Entry` and `Use when` columns.
* Link each active entry once; paths are relative to the index.
* Replace example rows with actual entries; use only the header and separator for an empty collection.
* Exclude session records, withdrawn entries, and the index itself.

```markdown
| Entry | Use when |
| --- | --- |
| [Repository instructions](repository-instructions.md) | Use when changing code or validating changes in this repository. |
```

## Knowledge entries

| Field | Required | Meaning |
| --- | --- | --- |
| `description` | Yes | Content and use in at most three short sentences. |
| `status` | Yes | `active`, `superseded`, or `deprecated`. |
| `superseded_by` | For `superseded` only | Replacement path relative to the entry. |

* `active` means current and useful; a hypothesis remains uncertain.
* `superseded` means replaced; follow `superseded_by` to current knowledge.
* `deprecated` means withdrawn without a replacement.
* Keep body content in short bullets; use sections only when useful.
* Add tables, snippets, reusable templates, or Mermaid and ASCII diagrams when they help.
* Preserve sources, rationale, and uncertainty alongside the knowledge.
* Use the [three article templates](skills/context-gather/references/entry-templates.md).

## How the skills work together

| Request | Route |
| --- | --- |
| Implement a change using repository conventions | Apply reads the index and relevant entries, then guides the change. |
| Save what we learned in this conversation | Gather collects session knowledge, writes new entries, reviews existing context, then updates the index. |
| Build initial project memory | Gather uses supplied context and accessible sources, then creates entries and the index. |
| Check the collection for stale or duplicated knowledge | Gather reviews the requested scope and repairs supported defects. |
| Import lessons from previous sessions | Import sessions loads the selected records and invokes gather. |
| Review context without editing files | Gather returns findings and proposed changes; no files are written. |

* Keep temporary progress and next steps in the task's plan or handoff.
* Preserve unresolved decisions; do not infer accepted intent from code alone.
* Do not copy secrets or raw transcripts into knowledge entries.
* A successful retrieval check does not prove a future agent will apply the knowledge correctly.

## Working with Context-Driven Engineering

* CDE discovery can reuse the knowledge and consequences identified by apply.
* CDE context maintenance and audits can use gather for writing and collection review.
* Saved session processing uses import sessions, followed by gather.
* Reuse supplied decisions and evidence; do not repeat their investigation merely to save them.

## Optional Codex hooks

* The [Codex integration](integrations/codex/README.md) adds a startup reminder and session registration.
* `SessionStart` reminds the agent of the three skill roles and the required index.
* `Stop`, `Interrupt`, `PreCompact`, and `SessionEnd` run `context_register_session.py`.
* Each session has one record under `.context/sessions/`.
* Registration stores metadata only; it does not read transcripts or invoke skills.
* Ignore `.context/sessions/` in Git; it is excluded from knowledge entries and the index.
* Use [context-import-sessions](skills/context-import-sessions/SKILL.md) to process selected checkpoints.

## Development checks

```text
python -m unittest discover -s tests -v
```

* Use `python3` where that is the Python 3 executable.
* Tests cover registration and checkpoint bookkeeping.
* Skill validation checks structure; it does not prove agent selection or knowledge quality.
