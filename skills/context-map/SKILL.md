---
name: context-map
description: Understand project knowledge and when it changes decisions or actions. Use to organize project guidance, choose navigation entry points, or fix context routing.
---

# Map Project Context

## Goal

Understand what project knowledge means, when it applies, and how it changes an agent's decisions or actions.
Organize access to that knowledge around the situations in which agents need it.

* Choose entry points and map structures from actual project needs.
* Use the smallest structure that preserves useful conditions and leads to the needed sources.
* Keep the knowledge and procedure steps at their existing sources.
* Preserve project requirements, evidence limits, and unresolved decisions.

## Steps

1. Understand the knowledge before choosing its place in a map.

* Identify the project and the scope of the request.
* Read the supplied article, document, entry, or procedure for its meaning.
* For a collection, use headings and existing navigation to select relevant content.
* Read enough of each selected source to understand its claim, conditions, and evidence.
* Identify the problem that the source addresses.
* Distinguish what the source states from what you infer about its use.
* Compare its assumptions with the project's constraints and accepted decisions.
* Use these questions to identify what the source contributes.

| Question | Identify | Example |
| --- | --- | --- |
| What problem does this knowledge address? | The situation and desired outcome | Repeated calculations delay a response. |
| What does the source explain or recommend? | A claim, constraint, decision, or procedure | Reuse a calculated result for a limited time. |
| Under which conditions does it apply? | Assumptions, boundaries, and exceptions | Reuse is acceptable only within the allowed freshness limit. |
| What supports the claim? | Evidence and its limits | Measurements concern one workload, not every request. |
| What would an agent do differently? | A decision, action, or check | Check freshness requirements before choosing a cache lifetime. |

* Treat the examples as illustrations, not project facts.
* Do not turn an article's recommendation into an accepted project rule.

2. Examine the reasoning with 5W and Socratic questions.

* Use 5W, or 5 Whys, when a claim does not explain why a recommendation fits the problem.
* Ask why the desired outcome matters.
* Ask why the proposed action could produce that outcome.
* Continue with another why only when the answer leaves a relevant cause or assumption unclear.
* Stop when the explanation supports a use condition or the available evidence cannot support another answer.
* Do not require five questions or invent answers to complete the sequence.

| Example why | Possible source-supported answer | Consequence for mapping |
| --- | --- | --- |
| Why reuse calculated results? | Repeated calculations contribute to response delay. | Consider the source for response-performance tasks. |
| Why can a previous result serve a new request? | The relevant inputs remain valid during reuse. | Include input validity in the use condition. |
| Why is that reuse period acceptable here? | The article does not establish the project's freshness requirements. | Consult the project contract before adopting the recommendation. |

* Use Socratic questions to challenge the interpretation where it can change the route.

| Question type | Ask yourself | Effect on the route |
| --- | --- | --- |
| Clarification | What does this term mean in this source? | Preserve its precise meaning in the condition. |
| Assumptions | What must be true for this advice to work? | Make relevant preconditions explicit. |
| Evidence | Why is this evidence sufficient for the claimed use? | Keep the condition within the evidence's scope. |
| Alternatives | Could another source or method satisfy the task with fewer assumptions? | Select the source that fits the actual need. |
| Consequences | What could fail if an agent applies this advice? | Add the necessary constraint or conditional source. |
| Counterexample | When would this recommendation be wrong or unnecessary? | Exclude that situation from the route. |

* Answer these questions from the available sources and project context.
* Ask the user only when a missing decision prevents a supported mapping choice.
* Use only questions that can change your understanding or the route.
* Do not produce a questionnaire for every source.

3. Derive situations in which the knowledge changes work.

* Name a concrete decision, action, or check that the knowledge changes.
* Identify the situation in which an agent needs that contribution.
* Identify a similar situation in which the contribution does not apply.
* Compare the contribution with existing knowledge for the same situation.
* If sources disagree, keep the disagreement explicit instead of choosing a new project policy.
* If no useful application emerges, leave the source outside the maps.
* A missing application is not a reason to invent a broad task category.

| Source content | Useful situation | Avoid |
| --- | --- | --- |
| An article explains cache lifetime trade-offs. | Choose a cache lifetime under freshness constraints. | Read this for all backend work. |
| A context entry records accepted freshness limits. | Change or diagnose the age of displayed data. | Replace the accepted limits with the article's example values. |
| A procedure defines how to isolate response delays. | Investigate a delayed response. | Run the procedure merely because its document exists. |

* Identify what an agent knows when it starts: a question, task, symptom, decision, or affected area.
* Use actual requests, recurring work, and source applications as evidence for these entry points.
* Use the following terms when translating situations into routes.

| Term | Meaning |
| --- | --- |
| Entry point | The recognizable situation from which an agent starts looking for guidance |
| Route | A connection from an entry point to sources, with any conditions needed to select them |
| Source | A document, section, available skill, or external reference that supplies relevant information |
| Task | A requested outcome or recurring kind of work |
| Procedure | An established sequence of actions with conditions and an expected result |
| Read first | The source needed to understand task constraints or choose the next action |
| Additional | A supporting source whose relevance depends on a stated condition |
| Extend when | The condition that makes an additional source necessary |

* A task can need knowledge without having an established procedure.
* Do not invent procedure steps to complete a route.
* One source can serve several situations.
* One task can need several sources.
* Stop discovery when the application is clear or a specific missing fact prevents a conclusion.

4. Choose entry points, map structures, and locations that fit those situations.

* Compare the identified situations with the project's existing navigation.
* Reuse effective entry points and structures.
* Choose labels that an agent can recognize from its request.
* Avoid making the agent translate a symptom into an invented task category.
* Use the following options as examples, not a required set.

| Agent starts with | Possible structure | Use it when |
| --- | --- | --- |
| A question | Question → answer source | The agent needs a specific fact or explanation. |
| A task | Task → Read first → Extend when | The outcome identifies prerequisites and conditional guidance. |
| A symptom | Symptom → first check → conditional source | The next source depends on an observed result. |
| A decision | Decision → constraints → criteria → evidence | The agent must compare options within accepted limits. |
| A change area | Area → contracts → dependencies → applicable checks | The affected component determines relevant obligations. |
| A need to discover knowledge | Source → Use when | The agent needs to identify what available knowledge can contribute. |

* Choose fields that preserve the conditions established during analysis.
* Do not create a map type merely because this skill lists it.
* Use one map when its entries need the same fields and selection rules.
* Separate maps when their entry points need different fields or navigation.
* Use branches when a source choice depends on an earlier answer or observation.
* Do not force dependent choices into an unconditional reading list.
* Keep a missing branch justification explicit as a knowledge gap.
* Do not invent diagnostic steps to complete a tree.
* Keep each map in one location.
* Reuse an existing index or guidance file when it fits the chosen structure.
* Preserve its filename and letter case.
* Place compact project routing in the applicable `AGENTS.md`.
* Link to a separate map when its detail would obscure the agent file's other instructions.
* Keep nested agent files within their directory scope.
* Avoid creating files when an existing location serves the need.
* Before changing an existing format, inspect its readers and writers, including installed skills and hooks.
* Preserve the old format when a dependency's migration remains outside scope.

5. Write routes that preserve the knowledge's conditions and authority.

* Link the section that supplies the needed knowledge.
* Include relevant sources from `.context/`, `docs/`, contribution guides, available skills, and external references.
* Keep facts and procedures at their sources.
* Write use conditions from the applications established in Step 3.
* Distinguish accepted requirements from advice, evidence, and unresolved choices.
* When a route needs Read first, select its source with this table.

| Candidate for Read first | Select it when | Make it conditional when |
| --- | --- | --- |
| Accepted constraint or decision | It determines which actions are valid. | Only a possible dependency makes it relevant. |
| Procedure | The task requires its established sequence. | Only a later stage or failure requires it. |
| Available skill | The skill owns the required procedure. | A stated condition determines whether the task needs it. |
| Explanation or study | The agent needs its reasoning before choosing an approach. | It helps compare alternatives after constraints are clear. |

* Read first applies to the matching situation, not every task in the project.
* Select several first sources only when the next action needs each one.
* Give additional sources explicit selection conditions.
* Link a known procedure or skill directly.
* Avoid requiring another map when the destination is already known.
* If no useful source exists, preserve the gap instead of adding filler.
* Use the examples below only where their structure fits.
* Replace fictional paths and conditions with verified project sources.

* Example: a source index at `.context/index.md` supports knowledge discovery.

```markdown
| Source | Use when |
| --- | --- |
| [Freshness limits](cache-freshness.md) | Change or diagnose the age of displayed data. |
| [Cache lifetime study](../docs/cache-study.md) | Compare cache lifetimes within accepted freshness limits. |
| [Response diagnosis](../docs/diagnosis.md#response-delays) | Investigate delayed responses. |
```

* Example: task routes in a root `AGENTS.md` identify prerequisites and conditional sources.

```markdown
## Task routing

Select the rows that match the task.
Reuse current information from the conversation.
Read the required sections without recursively reading every linked document.
Stop when the outcome, constraints, and required evidence are clear.
Expand the search for missing information, conflicts, or changed scope.

| Task | Read first | Extend when |
| --- | --- | --- |
| Choose a cache lifetime | [Freshness limits](.context/cache-freshness.md) | Read the [cache study](docs/cache-study.md) when comparing lifetimes within those limits. |
| Select checks for a change | [Validation scope](docs/testing.md#validation-by-change-scope) | Read [evidence reuse](docs/testing.md#evidence-reuse) when considering previous results. |
```

* Example: a symptom route in a root `AGENTS.md` selects guidance from an observed result.
* Its branches require support from the linked diagnosis procedure.

```markdown
## Displayed data appears stale

Start with the [age check](docs/diagnosis.md#check-data-age).
Compare the observed age with the [accepted limit](.context/cache-freshness.md).

* If the age exceeds the limit, use [refresh diagnosis](docs/diagnosis.md#refresh-failures).
* If the age meets the limit, use [freshness expectations](docs/diagnosis.md#freshness-expectations).
* If the age cannot be established, use [measurement gaps](docs/diagnosis.md#measurement-gaps).
```

* These examples are alternatives that can coexist when the project needs them.
* Do not copy all examples as a default architecture.
* Add local selection and stopping guidance only where agents need it.
* Do not make maps require each other as repeated navigation steps.
* Do not require knowledge-entry metadata on ordinary documents.
* Exclude raw transcripts, secrets, and temporary progress records.

6. Check that the chosen structure leads to the intended knowledge.

* Compare each route with the source's claim, conditions, authority, and evidence limits.
* Start from realistic requests without assuming the agent already knows the destination.
* Check a matching situation and a similar situation that should not select the route.
* Check each conditional branch against its supporting source.
* Check where reading stops and what would justify expanding it.
* Check combined routes when a task needs several sources.

| Example request | Expected selection | Meaning to preserve |
| --- | --- | --- |
| Find the accepted freshness limit | Question route or source index: freshness limits | Find the project decision without reading the cache study. |
| Choose a cache lifetime | Task map: freshness limits, then the cache study when needed | Advice from a study does not override accepted constraints. |
| Investigate displayed data within the freshness limit | Symptom route: freshness expectations | Do not select refresh-failure guidance without its condition. |
| Fix a spelling error in a document | Local text and applicable writing guidance | A nearby performance topic does not activate a diagnostic procedure. |

* Treat these examples as expected choices, not evidence of completed agent runs.
* Fix routes that omit necessary information or select unrelated sources.
* Repeat the affected checks after a fix.
* Check selection without executing destination procedures.
* Check file paths, section anchors, external sources, and skill availability.
* Write local paths relative to the file that contains each map.
* For retired entries, follow valid replacement paths.
* Keep broken replacements, cycles, and inaccessible sources explicit as unresolved gaps.
* Do not present unchecked destinations as established routes.
* Preserve substantive knowledge and unrelated instructions when removing duplicate navigation.
* Save the maps within the user's authorized scope.
* If the user requests suggestions only, return proposed maps without editing files.
