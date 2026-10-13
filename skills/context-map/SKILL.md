---
name: context-map
description: Understand project knowledge and when it changes decisions or actions. Use to organize project guidance, choose navigation entry points, or fix context routing.
---

# Map Project Context

## Goal

Understand what project knowledge means, when it applies, and how it changes an agent's decisions or actions.
Organize access to that knowledge around the situations in which agents need it.
Help agents narrow a broad request to relevant sources across the project's knowledge areas.

* Choose entry points and map structures from actual project needs.
* Use the smallest structure that preserves useful conditions and leads to the needed sources.
* Keep the knowledge and procedure steps at their existing sources.
* Preserve project requirements, evidence limits, and unresolved decisions.

## Steps

1. Understand the knowledge before choosing its place in a map.

* Identify the project and the scope of the request.
* Read the supplied article, document, entry, or procedure for its meaning.
* For a collection, use headings and existing navigation to select relevant content.
* Identify its knowledge areas and the needs that lead agents to each area.
* Inspect selected sources to understand those needs without loading the entire collection.
* Read enough of each selected source to understand its claim, conditions, and evidence.
* Identify the problem that the source addresses.
* Distinguish what the source states from what you infer about its use.
* Compare its assumptions with the project's constraints and accepted decisions.
* Use these questions to identify what the source contributes.

| Question | Identify | Example |
| --- | --- | --- |
| What does this source help an agent understand or do? | Its subject, purpose, and contribution | A use case explains expected behavior. A build guide explains how to compile a target. |
| What does it actually establish? | An explanation, requirement, decision, recommendation, or procedure | An architecture decision assigns component responsibilities. An article recommends an approach. |
| What request or uncertainty would make an agent need it? | A recognizable reason to seek this knowledge | Determine whether reported behavior is a defect. Find the build instructions for a target. |
| What does an agent need to know before using it? | Prerequisites and relevant project context | The target platform selects the build instructions. Product requirements constrain a design choice. |
| What supports it, and what limits its use? | Authority, evidence, assumptions, scope, and exceptions | A project decision governs one subsystem. A study measures only one workload. |
| How does it relate to other project knowledge? | Complementary sources, dependencies, overlaps, or conflicts | A use case defines behavior. A component contract constrains its implementation. |
| What can the agent decide or do after reading it? | The useful result of consulting the source | Select the applicable checks. Explain expected behavior in an issue response. |

* Use the questions that help you understand the source.
* Do not require a separate answer to every question.
* Continue when the application and its limits are clear.
* If they remain unclear, read the relevant source section or preserve the gap.
* Do not invent an application to complete a route.

* Treat the examples as illustrations, not project facts.
* Do not turn an article's recommendation into an accepted project rule.

2. Derive situations in which the knowledge changes work.

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

3. Choose entry points, map structures, and locations that fit those situations.

* Compare the identified situations with the project's existing navigation.
* Reuse effective entry points and structures.
* Choose labels that an agent can recognize from its request.
* Explain when an area matters instead of using directory names as the only selection cues.
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
* Provide orientation when agents need to discover which knowledge areas exist.
* Provide narrower routes when an area contains more knowledge than a request needs.
* Provide direct routes for recognizable needs with known destinations.
* Combine these navigation methods where useful, without requiring separate maps or a fixed reading order.
* Add a navigation level only when it helps select among sources or avoid unrelated reading.
* Connect areas when a request can need knowledge from several of them.
* State what makes another area relevant instead of requiring every area at the start.
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

4. Write routes that preserve the knowledge's conditions and authority.

* Link the section that supplies the needed knowledge.
* Include relevant sources from `.context/`, `docs/`, contribution guides, available skills, and external references.
* Keep facts and procedures at their sources.
* Write use conditions from the applications established in Step 2.
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

* Example: navigation in a root `AGENTS.md` covers different kinds of project knowledge.
* Some destinations supply guidance directly, while others help select a narrower source.

```markdown
## Find project guidance

Use a known relevant source directly.
Otherwise, select the area that matches the information you need.

| Information needed | Start here | Narrow the selection by |
| --- | --- | --- |
| Expected product behavior | [Use cases](.context/product/index.md) | User outcome and affected scenario |
| Component responsibilities or dependencies | [Architecture](.context/architecture/index.md) | Affected boundary or design decision |
| Implementation conventions | [Programming guide](docs/programming.md) | Language and kind of change |
| Compilation or local execution | [Build guide](docs/build.md) | Target and environment |
| Evidence needed for a change | [Validation guide](docs/testing.md#validation-by-change-scope) | Changed behavior and affected boundaries |
| How to answer an issue | [Response guidance](.context/collaboration/issue-responses.md) | Response purpose and available evidence |

Select relevant entries within an area without reading every linked document.
Consult another area when the current question requires its knowledge.
Stop expanding when the relevant outcome, constraints, and evidence requirements are clear.
```

* Within the product index, route by user outcomes rather than listing every document without use conditions.
* For a behavior change, use the relevant use case to establish the expected outcome.
* Consult architecture when the change affects component responsibilities or dependencies.
* Select validation guidance when deciding how to check the change.
* Consult response guidance when preparing an issue response, not merely because work began with an issue.
* A compilation request can go directly to the build guide without visiting product or architecture indexes.
* These paths illustrate selection across areas, not a required workflow for every change.

* These examples are alternatives that can coexist when the project needs them.
* Do not copy all examples as a default architecture.
* Add local selection and stopping guidance only where agents need it.
* Do not make maps require each other as repeated navigation steps.
* Do not require knowledge-entry metadata on ordinary documents.
* Exclude raw transcripts, secrets, and temporary progress records.

5. Check that the chosen structure leads to the intended knowledge.

* Compare each route with the source's claim, conditions, authority, and evidence limits.
* Start from realistic requests without assuming the agent already knows the destination.
* Check the whole path from a broad request to a specific source, including any local index.
* Check a request that needs several areas and a request that can use a direct route.
* Remove navigation steps that add no useful selection.
* Check a matching situation and a similar situation that should not select the route.
* Check each conditional branch against its supporting source.
* Check where reading stops and what would justify expanding it.
* Check combined routes when a task needs several sources.

| Example request | Expected selection | Meaning to preserve |
| --- | --- | --- |
| Find the accepted freshness limit | Question route or source index: freshness limits | Find the project decision without reading the cache study. |
| Choose a cache lifetime | Task map: freshness limits, then the cache study when needed | Advice from a study does not override accepted constraints. |
| Change behavior that crosses a component boundary | Relevant use case, affected architecture contracts, and applicable validation guidance | Select relevant sections without loading every area at the start. |
| Compile the project locally | Build guide for the target and environment | Skip unrelated product and architecture indexes. |
| Answer an issue without changing code | Response guidance and sources needed for the factual answer | Do not activate implementation and build procedures automatically. |
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
