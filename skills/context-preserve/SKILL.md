---
name: context-preserve
description: Use to preserve project decisions and findings from available sessions or supplied sources. Record established knowledge with its scope, rationale, and evidence.
---

# Preserve Project Context

## Goal

Preserve project decisions and findings with their meaning, scope, rationale, and evidence intact.

## Steps

1. **Identify what the available material establishes.**

* Identify knowledge that can guide future project work.
* Review the whole available session and supplied sources within the requested scope.
* Use the questions below to identify knowledge worth preserving.

| Question | Identify | Example |
| --- | --- | --- |
| What understanding or decision emerged or changed? | Goals, explanations, decisions, requirements, and corrections | The user clarified which component owns retries. |
| What did the work teach us? | Findings, effective procedures, failures, and their conditions | Repeated diagnosis revealed a useful sequence of checks. |
| Why does this knowledge apply, and what supports it? | Rationale, sources, scope, and evidence | A decision defines intended behavior. A test shows observed behavior. |
| What remains unresolved? | Proposals, uncertainty, and conflicting claims | The cause remains uncertain despite a successful recovery. |
| When could this knowledge help again? | Future situations where the knowledge affects work | A similar failure can use the established diagnostic sequence. |

* Identifying useful knowledge matters more than matching the table. Add or combine questions to identify knowledge the table does not fully cover.
* Continue when you understand which knowledge merits preservation, what it establishes, and what limits its use.

2. **Identify the relationships needed to preserve meaning.**

* Identify relationships that future readers need to understand and use the knowledge.
* Use the knowledge from Step 1 and directly related sources.
* Use the table to connect relevant statements with their purpose, consequences, and evidence where sources support these relationships.

| Aspect | Questions | Example |
| --- | --- | --- |
| Intent | Which goal or need explains this knowledge? Which priorities or exclusions follow from that goal? | Explicit unavailable states help users distinguish missing data from zero. |
| Behavior | Which expected behavior does it define or constrain? Under which conditions does that behavior change? | A missing reading must remain visibly unavailable. |
| Architecture | Which responsibility or dependency does it establish or affect? Which other components depend on that responsibility? | The provider reports availability. The browser presents it. |
| Contracts | Which boundary guarantees does it depend on or establish? Which assumptions must callers and providers share? | An absent value must not become zero during transport. |
| Implementation | Which code or configuration realizes or contradicts it? Which implementation details explain the observed result? | The decoder retains absent values instead of supplying defaults. |
| Evidence | Which observations support or challenge these relationships? What do these observations leave untested or uncertain? | A controlled test showed an unavailable reading. Mobile readability remains untested. |

* Identify relationships needed to understand or apply the knowledge, even when the table does not cover them. Add or adapt questions to identify those relationships.
* Keep gaps and disagreements explicit, including differences between intended behavior and observed results.
* Continue when you understand which relationships must accompany the knowledge and what supports or limits them.

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
* Combine location and form choices as needed. Different abstraction levels do not require separate files or prescribed document structures.
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

