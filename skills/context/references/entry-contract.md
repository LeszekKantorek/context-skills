# Entry contract

Use this reference when creating or updating `.context/` entries. The contract describes information, not a folder tree.

## Retrieval index

`.context/INDEX.md` is a short list. Each line has only a link (whose text is the entry title) and a `Use when…` instruction of at most two sentences. Do not add tags, types, status, summaries, or other metadata to index lines. Grouping is optional.

```markdown
# Context index

- [Signed local release](operations/local-release.md) — Use when producing a signed local build.
- [Read model](architecture/read-model.md) — Use when changing event projections or read-side consistency.
```

Index links are relative to `INDEX.md`. Make `Use when…` specific enough to select an entry without opening every file. List `active` and `observed` entries; keep `superseded` entries as files when their history matters, but remove them from the index and link to them from a replacement.

## Entry minimum

Start each entry with YAML frontmatter containing `description` and `status`. `description` summarizes what the entry contains and its relevant scope in no more than four sentences; it is not another `Use when…` instruction. Use `status: observed` for a potentially useful claim seen but not yet confirmed, `active` for supported current guidance, and `superseded` for retained history that should not guide new work. An `observed` entry is a lead to check, never an instruction to trust. Promote it to `active` only after confirming the claim; if contradicted, correct or remove it. Keep evidence, validation details, and any replacement link in the body only when useful. No tags or type field are required.

```markdown
---
description: Steps and checks for signing a local desktop build.
status: active
---

# Signed local release

Source: `scripts/release.sh`, issue #42.

## Procedure
...

## Checks and stop conditions
...
```

The body should answer only what a future agent needs. Keep one topic per file. Name by stable subject; use a date and issue identifier when two events or decisions might otherwise collide in parallel work.

## Writing gate

Before writing, ask:

1. What future task will retrieve this?
2. What decision or action changes because of it?
3. What supports the claim, and what could make it stale?
4. Is the same information already in `.context/`, a nearby source file, or the project's instructions?
5. Is it safe to share with every reader of this repository?

If there is no concrete future use, leave the candidate out. If a single observation could plausibly affect future work, keep it as `observed` with its evidence and uncertainty in the body; otherwise leave it in task notes. If an existing entry covers the subject, update it and its index instruction instead of adding a near duplicate.

Entry files are the source of truth. If an index line conflicts with a file, verify the file and repair the index. Preserve another contributor's unresolved change; reconcile evidence before overwriting it.
