# context-skills

Version: 1.1.0

Skills for AI agents to preserve project knowledge, organize it, and make it useful in future work. They work with your existing documents, decisions, and procedures.

## Skills

| Skill | Purpose |
| --- | --- |
| [context-preserve](skills/context-preserve/SKILL.md) | Preserve decisions and findings from sessions or supplied sources, including their rationale and evidence. |
| [context-review-sessions](skills/context-review-sessions/SKILL.md) | Find and review project sessions through context-preserve. |
| [context-map](skills/context-map/SKILL.md) | Build maps that connect tasks and questions to relevant documents or sections. |
| [context-retrieve](skills/context-retrieve/SKILL.md) | Locate relevant project sources with verified references and brief descriptions. |
| [context-maintain](skills/context-maintain/SKILL.md) | Review and improve the coherence and organization of existing project knowledge. |
| [context-diagnose](skills/context-diagnose/SKILL.md) | Investigate agent mistakes, apply targeted corrections, and check their effects. |
| [context-compile](skills/context-compile/SKILL.md) | Turn established project procedures into directly selectable skills. |

## Install the plugin from GitHub

```sh
codex plugin marketplace add LeszekKantorek/context-skills --ref main
codex plugin add context-skills@context-skills
```

## Install with the skills CLI

```sh
npx skills add LeszekKantorek/context-skills
```
