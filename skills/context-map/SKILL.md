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

2. Identify the roles that knowledge can serve in project navigation.

* Classify relevant content with the table below.
* Identify the situation in which an agent needs that contribution.
* Use actual requests, recurring work, and source applications to support the mapping.

| Term | Meaning | Recognize when | Routing use |
| --- | --- | --- | --- |
| Knowledge area | A group of related knowledge serving recognizable needs | Sources concern related questions, responsibilities, or work | Provide an entry point with conditions for choosing that area. |
| Task | An outcome an agent needs to achieve | The content supports a concrete request or recurring kind of work | Connect the requested outcome to relevant guidance. |
| Explanation | Knowledge that helps an agent understand a subject | The content explains concepts, mechanisms, or relationships | Route questions or missing understanding to this source. |
| Requirement or constraint | A condition that valid work must satisfy | The content defines required behavior, boundaries, or obligations | Route work affected by that condition to this source. |
| Decision | An accepted choice with its scope and rationale | The content records what the project chose and why | Route choices affected by that decision to its rationale and limits. |
| Procedure | An established sequence for achieving a result | The content gives actions, prerequisites, and an expected result | Provide a direct route when the requested work matches the procedure. |
| Evidence | Support for a claim or conclusion | The content supplies observations, measurements, or test results | Link it where an agent needs to assess a claim or compare options. |
| Open question | An unresolved matter relevant to the work | The content records missing knowledge, uncertainty, or conflicting positions | Make the uncertainty visible on affected routes. |

* Classify the relevant fragment rather than assigning one role to an entire document.
* Allow a fragment to serve several roles without copying its content.
* Use these roles to recognize applications, not to require folders or separate maps.
* Preserve useful knowledge even when none of these roles fits exactly.
* Do not treat an author's recommendation as a project requirement or accepted decision.
* Compare contributions from sources that address the same situation.
* Preserve disagreements instead of choosing a new project policy.
* Identify a similar situation in which the contribution does not apply.
* If no useful application emerges, leave the source outside the maps.
* Do not invent a broad task category or procedure to complete a mapping.
* Stop discovery when the application is clear or a specific missing fact prevents a conclusion.

3. Choose navigation that fits how agents seek project knowledge.

* Compare the needs identified in Step 2 with the project's existing navigation.
* Identify what an agent knows when it starts and what it still needs to find.
* Use the table to choose useful navigation methods.

| Navigation method | Meaning | Choose when | Apply by |
| --- | --- | --- | --- |
| Orientation | Show available knowledge areas and when they matter | The agent can describe its need but does not know where relevant knowledge lives | Describe areas through the needs they serve, with links to relevant sources or local maps. |
| Narrowing | Reduce a broad selection to relevant knowledge | An area contains more information than the request needs | Organize choices by meaningful differences, such as user outcome, component, target, or environment. |
| Direct route | Connect a recognizable need to a known destination | A recurring question or task has an established source | Link directly to the relevant section, procedure, or skill. |
| Conditional route | Select a destination according to a relevant condition | Different circumstances require different sources | State the condition that distinguishes each destination. |
| Connection between areas | Make related knowledge accessible across area boundaries | A request can require knowledge from several areas | Explain when another area becomes relevant and link to its appropriate entry point. |

* Combine methods where they help the same request.
* Do not require a separate map for each method or a fixed reading order.
* Reuse existing navigation when it supports the identified needs.
* Use one map when entries share useful selection criteria.
* Separate maps when their content needs different selection criteria or levels of detail.
* Add a navigation level only when it helps select sources or avoid unrelated reading.
* Choose labels that agents can recognize without knowing document names.
* Keep each map in one location.
* Place compact project routing in the applicable `AGENTS.md`.
* Link to a separate map when its detail would obscure other instructions.
* Preserve directory scope and existing filename conventions.
* Check readers and writers before changing a format that tools depend on.

4. Write tables that map situations to documents or sections.

* Create or update the tables selected in Step 3.
* Choose columns that support the selected navigation methods.
* Use the table below to select columns, not as a required output template.
* Make each row connect a recognizable situation to relevant document or section links.

| Column | Meaning | Include when | Write as | Useful for |
| --- | --- | --- | --- | --- |
| Situation / Task | The need or work that makes the linked documents relevant | The table starts from what the agent needs to do or understand | A recognizable request, outcome, or situation | Direct routes, conditional routes, orientation |
| Use when | The condition under which the linked document applies | The table starts from documents, or situations need a more precise condition | A concrete need, scope, or circumstance | Source indexes, conditional routes |
| Document / Section | The destination that supplies relevant knowledge | The mapping does not need separate prerequisite and additional sources | A document link, with a section anchor when appropriate | Direct routes, orientation, narrowing |
| Read first | The source required before the agent can proceed | The situation has a knowledge prerequisite | Links to documents or sections that establish necessary context or constraints | Task routes, conditional routes |
| Additional reading | Further sources needed under specific conditions | Only some instances of the situation need more knowledge | A condition paired with a document or section link | Conditional routes, connections between areas |
| Narrow by | The criterion for selecting within the linked collection | The destination is an index or document covering several possibilities | A relevant distinction, such as component, user outcome, target, or environment | Orientation, narrowing |

* Use either Situation / Task or Use when when one column sufficiently explains relevance.
* Use Read first and Additional reading instead of Document / Section when the distinction matters.
* Keep additional reading conditions beside their links.
* Link to the relevant section instead of requiring the whole document when possible.
* Keep knowledge and procedure steps in the linked documents.
* Do not add a column unless it helps select the right source.
* Preserve useful existing column names when their meaning fits the selected role.
* Extend when can name the Additional reading column when each cell pairs a condition with its link.
* Put general instructions for continuing or stopping navigation beside the table when needed.
* Write use conditions from the applications established in Step 2.
* Assign Read first from the situation's needs, not the document's category alone.
* Select several first sources only when the next action needs each one.
* Include relevant documents from `.context/`, `docs/`, contribution guides, available skills, and external references.
* Link a known procedure or skill document directly.
* Distinguish accepted requirements from advice, evidence, and unresolved choices.
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
