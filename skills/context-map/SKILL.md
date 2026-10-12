---
name: context-map
description: Create or update source maps and task maps. Use to organize project knowledge and task guidance, not to execute mapped tasks.
---

# Map Project Context

* Build a source map that answers: "Where is the knowledge for this situation?"
* Build a task map that answers: "Where do I start this task, and when do I need more information?"
* Keep definitions, examples, and instructions in this skill document.
* Preserve project requirements and unrelated content.
* For a report-only request, propose changes without editing files.

## Steps

1. Select the maps and their locations.

* Use the project and scope from the user's request.
* If the user does not name a project, use the current project.
* Read the applicable `AGENTS.md` and existing maps.
* Use the table to select which maps need work.

| Need | Map | What each row represents |
| --- | --- | --- |
| Find knowledge about a subject or constraint | Source map | A source and the conditions that make it useful |
| Select guidance for a recurring task | Task map | A task, its first source, and conditional additional sources |
| Improve both discovery and task guidance | Both maps | Two views of the same source content |

* Reuse the existing source index, including its filename and letter case.
* If no source index exists, use `.context/index.md` unless the user specifies another location.
* Put a new task map in the applicable `AGENTS.md`.
* If the project already maintains task guidance elsewhere, update that map instead of creating a duplicate.
* In that case, keep one link to the task map in `AGENTS.md`.
* Keep nested agent files within their directory scope.
* Update only the requested scope.

2. Identify the tasks, procedures, and sources.

* Find candidate sources through file listings, headings, existing links, and supplied tasks.
* Read the sections that establish their purpose and conditions.
* Include useful sources outside `.context/`, such as contracts, contribution guides, available skills, and external specifications.
* Use these definitions consistently.

| Term | Meaning | Example |
| --- | --- | --- |
| Source | A document, section, available skill, or external specification that supplies relevant information | An API contract section about response states |
| Task | A requested outcome or recurring kind of work | Diagnose a delayed API response |
| Procedure | An established sequence of actions with conditions and an expected result | Reproduce the delay, isolate its cause, and check the fix |
| Read first | The source needed to understand the task's constraints or select its procedure | A diagnostic procedure for response failures |
| Extend when | A condition that makes an additional source necessary | Read the queue contract when the delay occurs before processing |

* A task does not need an existing procedure to qualify for the task map.
* A contract or decision can be the first source when it supplies the information needed to proceed.
* A procedure can serve several tasks.
* One task can require several sources.
* Do not invent a procedure to complete a table row.
* Exclude raw transcripts, secrets, and temporary progress records.
* Preserve uncertainty when source content states a hypothesis or an unresolved decision.
* Stop discovery when you identify a supported destination or a specific unresolved issue for each task.
* Expand discovery only for missing information, conflicts, or dependencies that can change a map.

3. Build or update the source map.

* Link each useful source to a concrete condition for reading it.
* Select the document or section that contains the information.
* Preserve existing column names when current tools depend on them.
* Do not require knowledge-entry metadata on ordinary documents.
* Do not add every repository file merely to complete an inventory.
* If sections of one document serve different situations, give those sections distinct conditions.

| Source content | Useful condition | Weak condition |
| --- | --- | --- |
| An API contract defines response states. | Change or diagnose API response states. | Work on the backend. |
| A testing guide defines when earlier results remain usable. | Decide whether previous test results still apply. | Run tests. |
| A decision explains ownership of a queue. | Change queue ownership or its consumers. | Read architecture. |

* Example source map at `.context/index.md`:

```markdown
| Source | Use when |
| --- | --- |
| [API contract](../docs/api.md#response-states) | Change or diagnose API response states. |
| [Diagnosis](../docs/diagnosis.md#response-failures) | Investigate failed or delayed responses. |
| [Queue contract](../docs/queue.md#ownership-and-delivery) | Change queue ownership or diagnose delivery delays. |
| [Evidence reuse](../docs/testing.md#evidence-reuse) | Decide whether previous test results still apply. |
```

* These paths illustrate a fictional project.
* Replace example paths and conditions with sources that exist in the target project.
* Keep facts and procedure steps in their sources.

4. Build or update the task map.

* Name each task through its outcome or affected behavior.
* Select the first source through the criteria below.
* Put additional sources behind explicit conditions.

| Candidate for Read first | Select it when | Put it under Extend when if |
| --- | --- | --- |
| Procedure | The task requires its established sequence. | Only a later stage or failure requires it. |
| Contract or accepted decision | Its constraints determine the next action. | Only one possible dependency makes it relevant. |
| Available skill | The skill owns the requested procedure. | The task needs that skill only under a stated condition. |
| General overview | The task requires orientation that specific sources do not supply. | It provides useful background but does not determine the next action. |

* Read first is a prerequisite for the matching task, not a command to read every first-source cell.
* Select a source that supplies useful information, rather than another map that only repeats the destination.
* If a source is already current in the conversation, do not require another read merely to satisfy the label.
* Use several first sources only when the task needs each one before its next action.
* If no useful first source exists, record the gap instead of adding a broad document as filler.
* Keep distinct task conditions when they require different starting points.

| Weak task | Useful task | Reason |
| --- | --- | --- |
| Backend work | Diagnose failed or delayed API responses | The condition identifies a problem and selects a diagnostic procedure. |
| Documentation | Update issue or PR acceptance records | The condition selects a specific contribution procedure. |
| Quality | Select checks for a code change | The condition identifies a decision with a defined source. |

* Example task map in a root `AGENTS.md`:

```markdown
## Task routing

Select the rows that match the task.
Use each applicable row when the task crosses boundaries.
Read the source sections needed for the next action.
Reuse current information from the conversation.
Use the [source index](.context/index.md) when no task row identifies the needed knowledge.
Links do not require recursive reading.
Stop when the outcome, constraints, and required evidence are clear.
Expand the search for missing information, conflicts, or changed scope.

| Task | Read first | Extend when |
| --- | --- | --- |
| Diagnose failed or delayed API responses | [Diagnosis](docs/diagnosis.md#response-failures) | Read the [API contract](docs/api.md#response-states) for state mismatches. Read the [queue contract](docs/queue.md#ownership-and-delivery) for delivery delays. |
| Select checks for a code change | [Validation scope](docs/testing.md#validation-by-change-scope) | Read [evidence reuse](docs/testing.md#evidence-reuse) when considering previous results. |
| Update issue or PR acceptance records | [Acceptance procedure](CONTRIBUTING.md#acceptance) | Read [manual checks](docs/testing.md#manual-checks) when criteria need manual evidence. |
```

* Use the source map for discovery when a task route is absent or insufficient.
* Use a known task route directly without reading the source map first.
* Do not make the source map and task map point to each other as mandatory reading steps.
* Both maps can link the same source because they answer different questions.
* Keep each map in one location instead of copying it into AGENTS and task guidance.

5. Save the maps and preserve their dependencies.

* Check files, section anchors, external sources, and skill availability before adding destinations.
* Write local links relative to the file that contains each map.
* For a skill destination, name its available invocation.
* Do not install or create destination skills as part of mapping.
* For a retired entry, follow its replacement path.
* Report missing replacements and replacement cycles.
* Do not present an unchecked destination as an established route.
* Preserve substantive knowledge and source history when removing old navigation.
* Before changing an existing map's format, inspect its readers and writers.
* Include installed skills and startup hooks in that dependency check.
* Update dependencies only within the requested scope.
* If a dependency requires the old format, preserve that format until its migration enters scope.
* Report incompatible readers or writers instead of claiming that the migration is complete.
* Current Apply, Gather, and the startup hook still depend on the legacy context index.
* Do not change those skills or integrations unless the user includes them in scope.

6. Check both map views with representative requests.

* Establish each request's required information from the source content.
* Select destinations through the relevant map.
* Compare the selected information with the required information.
* Check both necessary sources found and unrelated sources avoided.
* For a local fix, use the original failing request and a similar request that should not select the route.

| Example request | Expected selection | Defect to detect |
| --- | --- | --- |
| Find the allowed API response states | Source map: API contract | The index requires a diagnostic workflow just to find a fact. |
| Diagnose a delayed response | Task map: diagnosis | The task requires reading the whole source index first. |
| Investigate a delay before queue delivery | Diagnosis, then queue contract | The conditional destination is missing. |
| Select checks using previous results | Validation scope, then evidence reuse | Previous results bypass the conditions for reuse. |
| Fix a typo in a local document | Local text and applicable writing guidance | An unrelated task route requires API diagnosis. |

* Treat these rows as examples of expected choices, not evidence of completed agent runs.
* If a required source is absent, add or change the relevant condition or destination.
* If a route selects unrelated information, narrow its condition.
* If navigation repeats, link the required source directly.
* If sources conflict, report the unresolved decision without inventing project policy.
* Repeat the affected checks after a fix.
* Check selection without executing destination procedures.

7. Report the changes and remaining issues.

* State which maps changed and where they reside.
* For each check, report the request, selected sources, and result.
* Distinguish inspection of a table from an observed agent run.
* List missing sources, unchecked destinations, conflicts, and remaining migration dependencies.
* For report-only work, return the proposed maps.
* Do not create a separate report file unless the user requests one.
* Leave knowledge gathering, content deduplication, document restructuring, session review, and procedure compilation outside this skill.
