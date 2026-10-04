---
name: context-review
description: Review the quality, discoverability, and actual use of .context, and repair scoped problems. Use for stale, conflicting, duplicated, or ignored knowledge, or a requested context workflow review. For recording one known finding, use context-consolidate.
---

# Review Context

Check whether project knowledge can support real decisions and actions. Tie findings to concrete use rather than a preferred folder tree or a documentation quota.

## Examine the collection and its use

1. Establish the requested scope and representative questions. Follow a full-coverage request; otherwise inspect what is needed and disclose sampling limits.
2. Try the project's retrieval paths. Exclude `.context/sessions/` from knowledge entries. Check relevant claims, their sources, contradictions, duplication, and applicability. Age alone does not prove staleness, and code does not automatically override accepted intent.
3. Check each in-scope entry's YAML frontmatter: required `description` and `status` (`active`, `deprecated`, or `superseded`); optional `related` as a list of entry-relative paths; `superseded_by` as an entry-relative path required for `superseded`. Check descriptions against content, link targets, and replacement cycles. Deprecated means withdrawn without a successor; superseded means replaced. An active entry may contain a clearly stated hypothesis.
4. Examine available usage evidence when relevant. Distinguish available knowledge, actual reading, declared application, and observable behavior. An opened entry can still be applied incorrectly. Without a relevant task or visible history, usefulness remains unknown; do not delete rare but important knowledge merely because it was not used recently.
5. Classify the cause and consequence: retrieval failure, obsolete knowledge, missing decision, uncertain claim, application error, or insufficient tools/evidence. Propose the smallest repair that addresses it.
6. Perform authorized repairs and recheck affected retrieval paths. In report-only mode, return proposed changes. Link repair can be mechanical; changing accepted meaning needs evidence and the proper decision authority.

## Repair without imposing a data model

Use `context-consolidate` for substantive updates when available. Otherwise apply the same small writing rule: preserve evidence and uncertainty, update the existing home, maintain the four-field frontmatter above, and keep useful replacement history. Do not add metadata, categories, or mandatory headings to make documents uniform. One useful note with minimal frontmatter can be sufficient.

Moving entries requires updating affected incoming and outgoing links. Resolve a duplicate only when its canonical home is clear. If authoritative claims still conflict, report the unresolved choice rather than silently superseding one. A metadata defect does not make the entire body false.

For a requested review of the skills or the complete workflow, read [workflow review](references/workflow-review.md). Ordinary collection review does not automatically authorize editing skill definitions, instructions, or hooks.

## Report findings with their limits

Give the questions checked, consequential findings with sources, repairs made or proposed, and remaining uncertainty. Report no material findings when justified. Separate working links, an authored retrieval rehearsal, observed compliance, and causal evidence of improvement; none establishes all the others.

Use existing task/session evidence rather than adding tracking by default. Do not schedule periodic reviews or contact other workers unless requested. When a wider CDE context audit includes `.context/`, return these findings once for that audit to reuse.
