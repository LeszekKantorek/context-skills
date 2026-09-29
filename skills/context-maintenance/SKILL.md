---
name: context-maintenance
description: >-
  Audit and repair an accumulated .context collection: duplicate or conflicting
  entries, stale claims, broken index links or Use when instructions, and excessive index or entry
  size. Use when memory feels bloated or unreliable, or for periodic maintenance.
  For new session learning use context-harvest.
---

# Context Maintenance

Keep the collection navigable and trustworthy without hiding history. Read `.context/INDEX.md`, then inspect only files needed to investigate a suspected problem. Measure entry and index size before making broad compaction claims.

Check for:

- broken links, `Use when…` instructions that match no meaningful task, active or observed entries missing from the index, and superseded entries still listed there;
- missing or misleading `description` frontmatter, invalid `status`, and descriptions longer than four sentences;
- duplicate claims or procedures that should share one canonical entry;
- claims contradicted by current code, tests, documentation, or an accepted decision;
- stale sources, dates, versions, or ownership assumptions;
- transient progress, copied logs, or whole transcripts;
- entries with several unrelated topics or sections that no longer affect action.

Fix mechanical index errors and clear duplicates when the canonical entry is unambiguous. Verify stale claims before editing them. Mark superseded decisions and lessons with a link to the replacement; preserve enough rationale to explain the history. Propose judgment-heavy merges, deletions of user-authored content, and large folder reorganizations with before/after paths and reasons.

Recheck `observed` entries that remain unconfirmed; correct or remove those contradicted by evidence or no longer useful. Use Git history to inspect prior edits instead of maintaining a separate change ledger.

Do not introduce fixed category folders during maintenance. Organize by how this project retrieves topics. Report what was verified, fixed, proposed, and left unresolved, including link counts or size changes when those motivated the pass.
