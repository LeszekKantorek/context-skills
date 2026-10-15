---
name: context-maintain
description: Use to review and reorganize existing project knowledge. Resolve duplication, fragmentation, and outdated content while preserving meaning, rationale, and scope.
---

# Maintain Project Context

## Goal

Improve the coherence and organization of existing project knowledge while preserving its meaning, rationale, evidence, and conditions of use.

## Steps

1. **Understand the collection and its uses.**

* Understand how the knowledge supports project work and how its sources relate.
* Use existing navigation and project guidance to find related sources across directories within the requested scope.
* Use the questions below to examine their contributions and dependencies.

| Question | Identify | Example |
| --- | --- | --- |
| What needs does this knowledge serve? | Questions, decisions, and work that depend on the collection | Release preparation uses both contribution guidance and a validation procedure. |
| Where does related knowledge appear? | Documents and sections that address the same responsibility or situation | Retry rules appear in a provider guide and an architecture decision. |
| What does each source contribute? | Requirements, explanations, procedures, evidence, and their conditions | A contract defines expected behavior; a test report records observed behavior. |
| Which sources establish the applicable decisions? | Accepted choices, rationale, exceptions, and replacements | A later decision replaces one platform's build procedure. |
| What depends on the current organization? | Incoming links, maps, references, and tools that read or write the content | A task map links directly to a section that may move. |

* Add questions when the table does not explain a source's contribution or relationships.
* Continue when the collection's uses and relationships are clear, with gaps explicit.

2. **Compare related knowledge and identify problems.**

* Identify problems that affect interpretation, maintenance, or use of the knowledge found in Step 1.
* Compare related statements by meaning, scope, rationale, authority, and supporting evidence.
* Check consequential claims against their sources when currency or correctness is in doubt.
* Use the table to distinguish problems from useful differences.

| Pattern | Examine | Interpretation |
| --- | --- | --- |
| Repeated knowledge | Do the statements establish the same rule under the same conditions? | Equivalent statements may duplicate one rule. Similar wording alone does not establish duplication. |
| Different scopes | Do different components, environments, or situations explain the difference? | Different conditions may justify separate rules. |
| Conflicting claims | Do the statements disagree under the same conditions? What establishes the intended result? | Incompatible claims under the same conditions indicate a conflict; its resolution may remain uncertain. |
| Outdated content | Has a decision, dependency, or observed behavior changed? | Evidence of change may establish obsolescence. Age alone does not. |
| Fragmented knowledge | Must readers reconstruct one explanation or procedure from scattered fragments? | Scattered fragments are a problem when readers must reconstruct context needed for one use. |
| Overgrown documents | Do independent subjects obscure the content needed for a particular situation? | Independent subjects are a problem when they obscure relevant knowledge or complicate maintenance. |
| Unnecessary instructions | Does a requirement still serve its stated purpose within its scope? | Repetition or a superseded purpose may indicate redundancy; an accepted obligation requires separate consideration. |
| Difficult access | Do links, section boundaries, or intermediate documents prevent selective reading? | Broken references or unnecessary navigation can prevent readers from reaching sufficient knowledge. |

* Identify other problems when the table does not explain an observed difficulty.
* Distinguish intended behavior from implementation observations. A disagreement does not establish which side needs correction.
* Continue when each identified problem has affected sources, an explained consequence, and supporting evidence or explicit uncertainty.

3. **Determine changes that preserve useful knowledge.**

* Choose changes that address the problems from Step 2 while retaining the contributions identified in Step 1.
* Determine where each affected statement, qualification, and supporting source will remain accessible.
* Use the table to choose changes suited to the content and existing organization.

| Change | Choose when | Preserve |
| --- | --- | --- |
| Keep and clarify | Similar statements have meaningful differences | Scope, conditions, and the reason each variant exists. |
| Consolidate | Several locations repeat equivalent knowledge | One maintained source, its rationale and evidence, with references from relevant locations. |
| Connect | Complementary knowledge belongs in separate sources | Links that explain the relationship and when the other source is needed. |
| Split | Independent subjects require different reading or maintenance | Enough context in each part, with links for shared constraints and dependencies. |
| Correct or replace | Evidence establishes an error or a superseding decision | The applicable knowledge, support for the correction, and useful decision history. |
| Remove | A fragment adds no unique knowledge or is demonstrably obsolete | Any still-useful rationale, evidence, exceptions, and references to its replacement. |
| Leave unresolved | Available evidence cannot settle a conflict or justify a change | Competing claims, their sources, and the decision or evidence still needed. |

* Choose another change or combine changes when these options do not preserve the knowledge's useful contributions.
* Select shared sources by responsibility and use, without imposing a new directory structure or document format.
* Separate supported editorial changes from proposals that alter accepted project decisions.
* Continue when changes have clear destinations, preserved qualifications, and identified effects on dependent references.

4. **Apply the selected changes and repair affected references.**

* Improve the collection using the changes selected in Step 3, within the current write scope.
* Establish destination content before removing fragments from their previous locations.
* Use the table to carry the selected changes through the affected documents and their dependents.

| Affected content | Action |
| --- | --- |
| Shared knowledge | Retain the complete meaning in the selected source and replace redundant copies with useful references. |
| Local qualifications | Keep conditions and exceptions beside the content they qualify, or link them with explicit applicability. |
| Rationale and evidence | Keep supporting sources and limitations attached to the claims they support. |
| Moved or replaced content | Update incoming links, section references, and existing replacement records. |
| Navigation | Repair affected routes. Use context-map when the change requires redesigning how situations lead to sources. |
| Dependent tools | Preserve required formats or update affected readers and writers within the authorized scope. |
| Unresolved proposals | Keep them distinguishable from accepted knowledge and identify what prevents their resolution. |

* Preserve other affected relationships when the table does not cover them.
* For a review without edits, present the proposed changes and unresolved matters instead of modifying the collection.
* Continue when selected changes are applied or presented, with incomplete work explicit.

5. **Check meaning, coherence, and access after the changes.**

* Check that the changes resolve the identified problems without losing useful knowledge or making it harder to reach.
* Compare the revised collection with the contributions from Step 1 and the changes selected in Step 3.
* Use representative needs from Step 1 to check whether readers can reach sufficient knowledge without unnecessary reading.
* Use the table to identify omissions, changed meanings, and remaining maintenance problems.

| Check | Expected result | Correction |
| --- | --- | --- |
| Knowledge coverage | Useful statements, rationale, evidence, and exceptions remain available | Restore missing content or references. |
| Meaning and authority | Scope and the distinction between decisions, observations, and proposals remain intact | Correct altered obligations, unsupported certainty, or lost conditions. |
| Coherence | Equivalent rules have a clear maintained source; meaningful variants remain distinguishable | Remove residual duplication or restore differences lost during consolidation. |
| Problem resolution | Each selected change addresses the problem that justified it | Adjust ineffective changes or retain the unresolved problem explicitly. |
| Access | Affected links and routes reach sufficient content for representative needs | Repair destinations, missing context, or unnecessary detours. |
| Dependent tools | Affected readers and writers remain compatible with the revised content | Correct incompatible changes or identify the remaining migration need. |

* Add a check when another consequence could affect interpretation, maintenance, or use.
* Correct problems and repeat affected checks.
* State remaining gaps and review limits without presenting unchecked content or proposed changes as verified.
