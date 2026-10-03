# context-skills

Gather, apply, consolidate, and review project knowledge in `.context/`.

The four skills support a context lifecycle, not a mandatory sequence. Read a known entry directly, use it in the current action, record durable learning when it occurs, and review the collection when there is a reason to question its quality or usefulness.

## Skills

| Skill | Use it for | Result |
| --- | --- | --- |
| [context-gather](skills/context-gather/SKILL.md) | Unknown, missing, scattered, or conflicting knowledge | Relevant sources, findings, and classified gaps |
| [context-apply](skills/context-apply/SKILL.md) | Using a known or readily found entry in the current task | A concrete consequence for the action, plan, or check |
| [context-consolidate](skills/context-consolidate/SKILL.md) | Initial collection, new learning, changed decisions, or selected session review | A small useful memory update, or no change |
| [context-review](skills/context-review/SKILL.md) | Stale, conflicting, hard-to-find, or misapplied context | Evidence-backed findings and scoped repairs |

Install the set with `npx skills add LeszekKantorek/context-skills`, or select one with `npx skills add LeszekKantorek/context-skills@context-apply` (likewise for the other names). Each skill includes its essential instructions; companions can be used when available without requiring the entire sequence.

## Memory belongs to the project

The project chooses filenames, folders, body layout, and navigation. Start with a useful note. Add an index, links, or topic folders when they help actual work. No index, category tree, or body template is required.

Each knowledge entry has a small YAML frontmatter:

| Field | Required | Meaning |
| --- | --- | --- |
| `description` | Yes | Short explanation of content and use |
| `status` | Yes | `active`, `deprecated`, or `superseded` |
| `related` | No | List of useful related-entry paths |
| `superseded_by` | When superseded | Path to the replacement entry |

Paths in `related` and `superseded_by` are relative to the containing entry. Relations need not be reciprocal. Keep links working after moving a file and avoid replacement cycles.

`active` means current and useful; an explicitly uncertain claim stays uncertain. `deprecated` means withdrawn without a direct successor. `superseded` means replaced by the linked entry. Sources, rationale, hypotheses, and evidence limits belong in ordinary prose.

```markdown
---
description: How to preserve an export snapshot when reopening a completed export.
status: active
related:
  - export-requests.md
---

# Reopening an export

Reopening preserves the snapshot associated with the accepted request.
Obtaining current data requires a new request. See the adopted product
decision for its rationale and applicability.
```

This is an illustrative form, not a required body template. [Entry examples](skills/context-consolidate/references/entry-examples.md) show different shapes, including uncertain observations and replacement links. The [writing prompts](skills/context-consolidate/SKILL.md#select-and-reconcile-knowledge) help choose what is worth retaining without turning information types into folders.

## From knowledge to action

For a snapshot requirement, gather finds the adopted decision and its basis. Apply connects it to behavior: reopening an export must retain its original snapshot. Consolidate records a new supported finding when it changes future work. Review asks whether later work can find and use the current rule.

A source being available, read, cited, or correctly applied are different observations. Passing implementation checks does not establish a good product effect. Preserve those distinctions and avoid claiming a skill caused an improvement without evidence.

Keep task progress, blockers, and next steps in the task's plan or handoff. Record only durable knowledge useful to future work. Do not store secrets or raw conversations in memory. An unresolved conflict between accepted decisions needs a decision within the appropriate authority. Report-only requests remain report-only; use existing authorization for requested updates.

## Working with Context-Driven Engineering

Context-skills gives CDE durable, retrievable project knowledge. CDE handles intent, investigations, decisions, implementation evidence, effects, and task coordination. Both can be used independently.

When both are present:

- CDE discovery reuses gather findings and application consequences.
- CDE context maintenance uses consolidate for a single update to `.context/`.
- CDE context audits reuse review findings without repeating the same scan.
- Experiments and adopted decisions may feed consolidation; task handoffs retain transient execution state.

No CDE installation or private research directory is required. This repository implements the context side of that relationship; it does not change a separately installed CDE library.

## Optional hooks and session review

The [Codex integration](integrations/codex/README.md) provides a short start reminder and session metadata registration:

- `SessionStart` reminds the agent to apply relevant context, gather missing knowledge, and consolidate durable learning.
- `Stop`, `Interrupt`, `PreCompact`, and `SessionEnd` run `context_queue_session.py`.
- Each session has one JSON record under `.context/sessions/`, with `session_id`, `updated_at`, `transcript_path`, and `reviewed_at`.
- Files have storage names such as `session-000001.json`. Identity comes from `session_id`, including after a file is renamed.
- Registration does not open transcripts, invoke a model, or schedule consolidation.

The `sessions/` directory is technical state, excluded from knowledge retrieval and frontmatter requirements. Ignore it in Git. Consolidate can review queued checkpoints using its [queue helper](skills/context-consolidate/scripts/scan_queue.py), or review explicitly supplied sessions without hooks.

## Development checks

The scripts use Python's standard library. Run from the repository root:

```text
python -m unittest discover -s tests -v
```

Use `python3` where that is the Python 3 executable. These automated checks exercise the hook and queue behavior. They do not evaluate an agent's skill selection, application of knowledge, or quality of consolidation. Structural validation does not by itself prove that an agent follows the skills.
