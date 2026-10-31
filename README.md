# context-skills

Skills for AI agents to preserve project knowledge, organize it, and make it useful in future work. They work with your existing documents, decisions, and procedures.

## Skills

| Skill | Purpose |
| --- | --- |
| [context-preserve](skills/context-preserve/SKILL.md) | Preserve decisions and findings from sessions or supplied sources, including their rationale and evidence. |
| [context-review-sessions](skills/context-review-sessions/SKILL.md) | Find and review project sessions through context-preserve. |
| [context-map](skills/context-map/SKILL.md) | Build maps that connect tasks and questions to relevant documents or sections. |
| [context-maintain](skills/context-maintain/SKILL.md) | Review and improve the coherence and organization of existing project knowledge. |
| [context-diagnose](skills/context-diagnose/SKILL.md) | Investigate agent mistakes, apply targeted corrections, and check their effects. |
| [context-compile](skills/context-compile/SKILL.md) | Turn established project procedures into directly selectable skills. |

Use the skill that fits the task; there is no required sequence.

## Install

```sh
npx skills add LeszekKantorek/context-skills
```

Choose the skills to install. Install `context-preserve` alongside `context-review-sessions`.

`context-review-sessions` finds sessions directly using available session information. If it cannot locate them, it asks for an ID or a location to search. It does not track which sessions have already been reviewed.
