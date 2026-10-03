# Entry examples

Choose prose and organization for the project. Only the small frontmatter contract is shared; these illustrative examples are not templates to fill in.

## A short procedure

```markdown
---
description: Where to find the local build signing steps before a release.
status: active
---

# Signing a local build

Follow the signing steps in `docs/release.md` before packaging. Keep that
document as the canonical procedure rather than copying its commands here.
```

## An uncertain observation

```markdown
---
description: A local export slowdown worth checking before changing batch size.
status: active
---

# Export batch size

In one local experiment, increasing the batch size made the export slower.
This is a lead, not a demonstrated production bottleneck. The task's experiment
record contains the inputs and measurements. Recheck representative data
before treating the observation as a reason to change the default.
```

`active` describes the entry's current usefulness. Its claim remains explicitly uncertain. Preserve an actual source pointer when recording a real observation.

## A replaced decision

```markdown
---
description: The withdrawn batch retry policy and why it was replaced.
status: superseded
superseded_by: retry-policy.md
related:
  - delivery-states.md
---

# Previous retry policy

The old policy retried the entire batch. The replacement distinguishes
accepted, rejected, and unknown outcomes. Keep the old reasoning here when
it explains why the policy changed; use the replacement for new work.
```

Use `deprecated` when withdrawing an entry without a successor, and explain the reason where useful. Omit `superseded_by` in that case.

`related` is a list of relative paths, and `superseded_by` is one relative path, both resolved from the containing entry. Preserve that meaning after moving a file. Relations need not be reciprocal. A replacement link must resolve and must not form a cycle. Do not manufacture links merely because two entries share a word.

Use the title in the body. Keep sources, applicability, accepted intent, and uncertainty where readers need them, without a required set of headings. If the project adds an index, keep it useful for navigation rather than a duplicate of all entry content.
