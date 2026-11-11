---
name: context-search
description: Use to locate and verify project sources relevant to a question before reasoning or planning. Search documentation, code, configuration, and other project text files.
metadata:
  version: "1.1.0"
---

# Search Project Sources

## Goal

Locate relevant sources and return verified references with brief descriptions and any information gaps.

When choosing how to run this skill, prefer a dedicated subagent if the question is likely to require several searches across files, following references, or substantial intermediate output. Give it the original question and search scope. Run the same procedure directly for simple lookups or when delegation is unavailable.

## Steps

### 1. Extract search terms

Use the question to choose starting points and determine what a relevant source must establish.

| Identify | What to look for | Example |
| --- | --- | --- |
| Subject | The main component, process, concept, or decision. | `delivery date` |
| Aspects | The properties, actions, relationships, reasons, and constraints that define what is requested. Include scope qualifiers such as dates and versions. | Why the `phase two` date changed and whether it was `approved`. |
| Exact references | Supplied identifiers, filenames, paths, symbols, versions, or quoted text. Preserve their spelling. | `REV-03` |

Group alternative wording by aspect. Use the groups to choose and refine searches. Evidence for different aspects can appear in different sections or files. Preserve the original qualifications when checking coverage. Keep the term analysis internal.

### 2. Grep & Follow relevant sources

* Use project maps, indexes, and known paths to scope the search. Start with exact references or distinctive subject terms. Use literal matching when the pattern is plain text. If `rg` is unavailable, use another search tool that can locate matching text and line numbers.
* Search related expressions as alternatives within a relevant scope. Use another aspect to narrow or redirect the search as evidence warrants.

For a question about SimConnect integration testing procedures, start with `SimConnect` and inspect the matching sources. If those sources point to `docs/testing/`, search there for wording used to describe tests.

```sh
rg -n -F -e 'SimConnect' docs/
rg -n -F -i -e 'testing' -e 'validation' -e 'tests' docs/testing/
```

A repository-wide OR query combining `SimConnect`, `testing`, `integration`, and `procedure` also matches unrelated tests and procedures. Use the filename, path, and enclosing heading to check whether a section concerns the subject, even when the matching line omits it.

| Option | Use |
| --- | --- |
| `-n` | Show line numbers. |
| `-F` | Match literal text. |
| `-i` | Match regardless of case when spelling case is immaterial. |
| `-e` | Supply a pattern. Repeat for alternatives or use it when a pattern starts with `-`. |
| `-g` | Include or exclude paths by glob. |
| `--hidden` | Include hidden files and directories, subject to ignore rules. |
| `--no-ignore` | Bypass ignore rules when relevant material is ignored. |

`rg` normally respects ignore rules and skips hidden paths during recursive searches. When a project map points to a hidden directory such as `.context/` or `.agents/`, scope the search to that directory and use `--hidden` as needed. Use `--no-ignore` only within a specific path when an ignore rule hides relevant material.

Open promising matches and read the surrounding section. Follow references that could establish a requested fact, including links to headings and references elsewhere in the source.

| Finding | Next action |
| --- | --- |
| Matches concern the subject but differ in scope | Narrow the search using a qualification from the question. |
| The selected sources contain no matches | Try alternative wording, then expand through related maps and references. |
| A source supplies a relevant term or reference | Follow it or use the term in another search if it helps answer the question. |
| A section answers only part of the question | Keep the section and use the remaining gap to choose the next search. |
| A match provides neither requested information nor a relevant lead | Move on to other matches. |
| A source cannot be opened | Record its location and the access problem. Check other available sources. |

Compare the verified findings with the original question. Continue while a useful lead could resolve a gap. Stop once the sources cover the request or the available leads are exhausted.

### 3. Report verified source locations

Return a compact message with project-relative paths, exact line ranges, and brief descriptions of what each source establishes. Check every range in the opened source before reporting it. Include `Not found` for unresolved information and `Unavailable` for relevant sources that could not be read. Omit either entry when it does not apply.

```text
- decisions/delivery-date.md:12-19 - Reasons for changing the phase two delivery date.
- plans/schedule.md:30-38 - Revised dates and the reference to decision D-17.
Not found: confirmation that the revised date was approved.
Unavailable: records/meeting-notes.md - access denied.
```
