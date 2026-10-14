---
name: context-preserve
description: Use to preserve project decisions and findings from available sessions or supplied sources. Record established knowledge at appropriate Context-V levels with its scope, rationale, and evidence.
---

# Preserve Project Context

## Goal

Preserve project decisions and findings at appropriate Context-V levels, with their meaning, scope, rationale, and evidence intact.

## Steps

1. **Identify what the available material establishes.**

* Identify knowledge that can guide future project work.
* Review the whole available session and supplied sources within the requested scope.
* Include user corrections, accepted decisions, verified findings, and unresolved matters that affect future work.
* Use the questions below to determine what each candidate establishes.

| Question | Identify | Example |
| --- | --- | --- |
| What did the work establish? | The decision, finding, correction, or unresolved matter | The user assigned retry ownership to the transport component. |
| Why will this matter again? | A future situation where the knowledge affects work | A provider change must preserve retry ownership. |
| What supports this knowledge? | The source and its authority | A user decision establishes intended ownership. Code shows current ownership. |
| Why does this choice apply? | The stated rationale and relevant alternatives | One retry owner prevents competing reconnect attempts. |
| Where does it apply? | Scope, conditions, and exceptions | The decision covers browser connections, not provider recovery. |
| What remains uncertain? | Assumptions, proposals, conflicts, and missing evidence | The team proposed a timeout but did not measure it. |

* Preserve useful knowledge even when these questions do not cover it. Add a question that resolves the missing distinction.
* Distinguish accepted decisions, observations, proposals, and hypotheses.
* Keep temporary progress in the task's plan or handoff.
* Continue when each candidate has a future use, an identifiable source, and explicit evidence limits.
* If no candidate qualifies, finish without creating content.

2. **Connect the knowledge through Context V.**

* Determine the abstraction levels and relationships needed to preserve the candidates from Step 1.
* Context V connects intent, behavior, architecture, contracts, and implementation with evidence at corresponding levels.
* Use the table to identify relevant levels and available evidence.

| Level | Knowledge to preserve | Corresponding evidence |
| --- | --- | --- |
| L1 — Intent | Purpose, expected value, users, and reasons | Outcomes or acceptance that address the original purpose |
| L2 — Behavior | Requirements, scenarios, and observable behavior | Observed scenarios or behavioral test results |
| L3 — Architecture | Responsibilities, boundaries, dependencies, and design rationale | Dependency inspection or integration evidence |
| L4 — Contracts | Interface promises, protocols, units, invariants, and state transitions | Contract checks, fixtures, or compatibility results |
| L5 — Implementation | Relevant facts about code, configuration, or algorithms | Source inspection, local tests, builds, or runtime observations |

* Preserve meaning when a candidate spans several levels or falls outside this model.
* Apply levels to relevant statements, not automatically to entire files.
* Connect statements where sources establish a relationship between purpose, behavior, responsibility, contract, or implementation.
* Distinguish planned checks from observed results.
* Read additional sources only when they can resolve a material gap or conflict in the selected knowledge.
* Keep missing rationale or evidence explicit. Do not invent intermediate decisions to complete the model.
* Continue when relevant relationships and evidence limits are clear.

3. **Record the knowledge in an appropriate form and location.**

* Preserve the selected knowledge and its relationships where future work can use them.
* Use known project locations and relevant navigation to inspect directly related content.
* Use the table to choose how to record each candidate.

| Existing content or knowledge need | Action | Example |
| --- | --- | --- |
| An existing source already preserves the knowledge | Reuse the source or add a necessary link | Link to the accepted ownership decision. |
| A relevant passage needs a correction or addition | Update that passage with the supported change | Add the agreed exception to the existing contract. |
| No known location fits the knowledge | Create a focused entry in the project's context location | Record the agreed recovery boundary with its rationale. |
| Understanding depends on an explanation | Explain the established concepts and relationships | Explain why source health differs from connection health. |
| Understanding depends on a comparison or structure | Use a table or diagram | Show component responsibilities and their boundaries. |
| The knowledge establishes an operating procedure | Record the established steps and their conditions | Preserve the verified recovery sequence and success check. |

* Choose another form or location when these options do not preserve the knowledge clearly.
* Combine location and form choices as needed. Context-V levels do not require separate files or prescribed document structures.
* Keep related statements together when future work needs them together.
* Preserve sources, rationale, scope, and uncertainty beside the relevant statements.
* Retain proposals as proposals and unresolved conflicts as unresolved conflicts.
* Limit changes to the selected knowledge and directly affected references.
* Continue when the records preserve the selected knowledge without unsupported additions.

4. **Check that the record preserves the established meaning.**

* Check whether future work can use the record without reconstructing the original conversation.
* Compare the changed content with the candidates from Step 1 and the relationships from Step 2.
* Use the table to identify and correct losses or distortions.

| Check | Problem signal | Correction |
| --- | --- | --- |
| Coverage | A selected decision, correction, or finding disappears | Restore the missing knowledge or retain a link to its existing source. |
| Meaning and authority | A proposal becomes a requirement or code becomes proof of intent | Restore the source's meaning and authority. |
| Scope | A local decision becomes a general rule | Restore conditions, boundaries, and exceptions. |
| Rationale and relationships | The record loses an established reason or dependency | Restore the explanation or source link. |
| Evidence | A planned check appears as a passing result | Separate expected evidence from observed results. |
| Uncertainty | The record silently resolves a conflict | Preserve the disagreement and the unresolved decision. |
| Future use | A reader cannot identify when the knowledge applies | State the relevant situation or condition. |
| References | A source link or affected reference no longer reaches its target | Correct the reference. |

* Add a relevant check when these checks do not cover a possible loss of meaning.
* Correct the affected content.
* Repeat the affected checks until the record preserves the selected knowledge and its limits.

