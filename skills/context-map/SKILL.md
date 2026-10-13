---
name: context-map
description: Understand project knowledge and when it changes decisions or actions. Use to organize project guidance, choose navigation entry points, or correct context routing.
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

* Build a mapping from situations to documents or sections as a table with two or more columns.
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

* Example column combinations:
* Paths in these examples are relative to a root `AGENTS.md`.

``` Use when | Document / Section
| Use when | Document / Section |
| --- | --- |
| Change or diagnose the age of displayed data. | [Freshness limits](.context/cache-freshness.md) |
| Compare cache lifetimes within accepted freshness limits. | [Cache lifetime study](docs/cache-study.md) |
| Investigate delayed responses. | [Response diagnosis](docs/diagnosis.md#response-delays) |
```

``` Task | Read first | Additional reading
| Task | Read first | Additional reading |
| --- | --- | --- |
| Choose a cache lifetime | [Freshness limits](.context/cache-freshness.md) | Read the [cache study](docs/cache-study.md) when comparing lifetimes within those limits. |
| Select checks for a change | [Validation scope](docs/testing.md#validation-by-change-scope) | Read [evidence reuse](docs/testing.md#evidence-reuse) when considering previous results. |
```

``` Situation | Document / Section | Narrow by
| Situation | Document / Section | Narrow by |
| --- | --- | --- |
| Determine expected product behavior | [Use cases](.context/product/index.md) | User outcome and affected scenario |
| Assess component responsibilities or dependencies | [Architecture](.context/architecture/index.md) | Affected boundary or design decision |
| Choose implementation conventions | [Programming guide](docs/programming.md) | Language and kind of change |
| Compile or run the project locally | [Build guide](docs/build.md) | Target and environment |
| Determine evidence needed for a change | [Validation guide](docs/testing.md#validation-by-change-scope) | Changed behavior and affected boundaries |
| Prepare an issue response | [Response guidance](.context/collaboration/issue-responses.md) | Response purpose and available evidence |
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

5. Check that the tables lead from situations to the right documents.

* Check the mappings against realistic requests and their linked sources.
* Use the table to identify and correct navigation problems.

| Check | Expected result | Problem signal | Correction |
| --- | --- | --- | --- |
| Recognizable situation | The agent can select a row from its request | Selection requires knowing the destination document first | Describe the situation through the need or work it serves. |
| Relevant destination | The linked content addresses the situation | The document shares a topic but does not supply the needed knowledge | Select a more relevant document or section. |
| Sufficient knowledge | The mapping supplies the information needed to proceed | A required constraint, explanation, or procedure is missing | Add the missing source with its use condition. |
| Selective reading | The mapping avoids unrelated content | Every request selects broad documents or unconditional additional reading | Narrow the link or state when additional reading matters. |
| Clear conditions | Similar situations select different sources when necessary | A row also matches situations where its guidance does not apply | Clarify its scope, conditions, or exceptions. |
| Useful navigation | Each intermediate map helps select the next destination | Navigation repeats, loops, or adds no useful choice | Remove the detour or link directly to the source. |
| Preserved meaning | The mapping respects the source's authority and limits | Advice appears mandatory or uncertain knowledge appears settled | Correct the wording and preserve the source's qualifications. |
| Valid destination | The link reaches the intended document or section | The path, anchor, or replacement is missing or incorrect | Correct the link or mark the unresolved gap. |

* Check a matching request and a similar request that should not select the same row.
* Include a request that needs several knowledge areas when the map supports such work.
* Check the full path when a row links to another index.
* Check selection without executing the linked procedures.
* Distinguish expected selections from observed agent behavior.
* Repeat the affected checks after correcting a mapping.
* Save changes within the requested scope.
