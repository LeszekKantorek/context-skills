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

* Use each step's conclusions in the next step without creating separate reports or intermediate documents.

1. Understand what the sources contribute.

* Establish what the sources contribute and when they can help project work.
* Use supplied sources and relevant project guidance within the requested scope.
* For collections, select relevant content through headings and existing navigation.
* Use the questions below to examine meaning, authority, conditions, and relationships.

| Question | Identify | Example |
| --- | --- | --- |
| What does this source help an agent understand or do? | Its subject, purpose, and contribution | A use case explains expected behavior. A build guide explains how to compile a target. |
| What does it actually establish? | An explanation, requirement, decision, recommendation, or procedure | An architecture decision assigns component responsibilities. An article recommends an approach. |
| What request or uncertainty would make an agent need it? | A recognizable reason to seek this knowledge | Determine whether reported behavior is a defect. Find the build instructions for a target. |
| What does an agent need to know before using it? | Prerequisites and relevant project context | The target platform selects the build instructions. Product requirements constrain a design choice. |
| What supports it, and what limits its use? | Authority, evidence, assumptions, scope, and exceptions | A project decision governs one subsystem. A study measures only one workload. |
| How does it relate to other project knowledge? | Complementary sources, dependencies, overlaps, or conflicts | A use case defines behavior. A component contract constrains its implementation. |
| What can the agent decide or do after reading it? | The useful result of consulting the source | Select the applicable checks. Explain expected behavior in an issue response. |

* Understanding the source matters more than completing the table. Ask another question when its contribution remains unclear.
* Distinguish source claims, your interpretation, and accepted project decisions.
* Continue when contributions, limits, and relationships are clear, with unresolved gaps explicit.

2. Connect source contributions to situations and useful knowledge roles.

* Connect the source contributions identified in Step 1 to recognizable situations so that navigation reflects actual project needs.
* Ground situations in actual requests, recurring work, and supported source applications.
* Use the table to identify useful roles and groupings.

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

* Preserving useful applications matters more than fitting the listed roles. Describe another role when none preserves the meaning.
* Assign roles to relevant fragments; one fragment can serve several roles.
* Compare sources for the same situation, preserving differences in scope and unresolved disagreements.
* Continue when each identified situation has relevant sources and use conditions, or an explicit source gap.

3. Determine how agents will reach relevant knowledge.

* Determine navigation methods for the situations identified in Step 2.
* Compare existing navigation with what agents know initially and what they need to find.
* Use the table to select navigation methods.

| Navigation method | Meaning | Choose when | Selected structure |
| --- | --- | --- | --- |
| Orientation | Show available knowledge areas and when they matter | The agent can describe its need but does not know where relevant knowledge lives | Areas described through the needs they serve, leading to sources or local maps. |
| Narrowing | Reduce a broad selection to relevant knowledge | An area contains more information than the request needs | Choices organized by user outcome, component, target, or environment. |
| Direct route | Connect a recognizable need to a known destination | A recurring question or task has an established source | A direct connection to the relevant section, procedure, or skill. |
| Conditional route | Select a destination according to a relevant condition | Different circumstances require different sources | Alternative destinations distinguished by explicit conditions. |
| Connection between areas | Make related knowledge accessible across area boundaries | A request can require knowledge from several areas | A connection to another area with the condition that makes it relevant. |

* Reaching relevant knowledge matters more than using a listed method. Adapt or combine methods when none serves the need.
* Reuse existing maps, separating them only when selection criteria or levels of detail differ.
* Keep compact routing in the applicable `AGENTS.md` and detailed maps in separate linked files.
* Check current format dependencies before replacing existing navigation. Preserve compatibility unless migration is within scope.
* Continue when navigation methods, map boundaries, locations, and compatibility constraints are clear.

4. Write tables that map situations to documents or sections.

* Build a mapping from situations to documents or sections as a table with two or more columns.
* Use the candidate mappings from Step 2 and the navigation choices from Step 3.
* Create or update tables in the selected locations.
* Make each row connect a recognizable situation to relevant document or section links.
* Use the table below to select columns, not as a required output template.

| Column | Meaning | Include when | Write as | Useful for |
| --- | --- | --- | --- | --- |
| Situation / Task | The need or work that makes the linked documents relevant | The table starts from what the agent needs to do or understand | A recognizable request, outcome, or situation | Direct routes, conditional routes, orientation |
| Use when | The condition under which the linked document applies | The table starts from documents, or situations need a more precise condition | A concrete need, scope, or circumstance | Source indexes, conditional routes |
| Document / Section | The destination that supplies relevant knowledge | The mapping does not need separate prerequisite and additional sources | A document link, with a section anchor when appropriate | Direct routes, orientation, narrowing |
| Read first | The source required before the agent can proceed | The situation has a knowledge prerequisite | Links to documents or sections that establish necessary context or constraints | Task routes, conditional routes |
| Additional reading | Further sources needed under specific conditions | Only some instances of the situation need more knowledge | A condition paired with a document or section link | Conditional routes, connections between areas |
| Narrow by | The criterion for selecting within the linked collection | The destination is an index or document covering several possibilities | A relevant distinction, such as component, user outcome, target, or environment | Orientation, narrowing |

* Clear situation-to-document mappings matter more than matching the listed columns. Adapt or add a column when necessary selection information does not fit.
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
* Preserve the authority and uncertainty established in Step 1 when wording each mapping.
* If no useful source exists, preserve the gap instead of adding filler.
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

* In the area example, a behavior question leads to the relevant use case through the product index.
* A change affecting component responsibilities also selects architecture guidance.
* A compilation request can select the build guide directly.
* Response guidance becomes relevant when preparing an issue response.
* These selections illustrate the example's intended behavior, not instructions to perform those tasks during mapping.
* Use only the example structures that fit the navigation selected in Step 3.

* Do not make maps require each other as repeated navigation steps.
* Do not require knowledge-entry metadata on ordinary documents.
* Exclude raw transcripts, secrets, and temporary progress records.
* Write local links relative to the file containing each table.
* Continue when the draft tables contain actual destinations and selection conditions, with missing sources explicit for validation.

5. Check that the tables lead from situations to the right documents.

* Establish whether the tables cover the identified needs and lead to sufficient knowledge without unnecessary reading.
* Work from the draft tables, the candidate mappings from Step 2, and the navigation choices from Step 3.
* Check the mappings against realistic requests and their linked sources.
* Use the table to identify and correct navigation problems.

| Check | Expected result | Problem signal | Correction |
| --- | --- | --- | --- |
| Coverage of needs | Each identified need has a mapping, a justified omission, or an explicit gap | A need from Step 2 disappears without explanation | Add a supported mapping or preserve the reason for omission or the unresolved gap. |
| Recognizable situation | The agent can select a row from its request | Selection requires knowing the destination document first | Describe the situation through the need or work it serves. |
| Relevant destination | The linked content addresses the situation | The document shares a topic but does not supply the needed knowledge | Select a more relevant document or section. |
| Sufficient knowledge | The mapping supplies the information needed to proceed | A required constraint, explanation, or procedure is missing | Add the missing source with its use condition. |
| Selective reading | The mapping avoids unrelated content | Every request selects broad documents or unconditional additional reading | Narrow the link or state when additional reading matters. |
| Clear conditions | Similar situations select different sources when necessary | A row also matches situations where its guidance does not apply | Clarify its scope, conditions, or exceptions. |
| Useful navigation | Each intermediate map helps select the next destination | Navigation repeats, loops, or adds no useful choice | Remove the detour or link directly to the source. |
| Preserved meaning | The mapping respects the source's authority and limits | Advice appears mandatory or uncertain knowledge appears settled | Correct the wording and preserve the source's qualifications. |
| Valid destination | The link reaches the intended document or section | The path, anchor, or replacement is missing or incorrect | Correct the link or mark the unresolved gap. |

* Reliable source selection matters more than completing the listed checks. Add a relevant check when a navigation problem falls outside them.
* Check a matching request and a similar request that should not select the same row.
* Include a request that needs several knowledge areas when the map supports such work.
* Check the full path when a row links to another index.
* Check selection without executing the linked procedures.
* Distinguish expected selections from observed agent behavior.
* Repeat the affected checks after correcting a mapping.
* Preserve omissions and gaps beside the affected mappings when useful, without creating a separate report.
* Save changes within the requested scope.
* Finish when the mappings pass the applicable checks and justified omissions or unresolved gaps remain visible.
