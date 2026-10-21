# context-skills

Skills for AI agents to preserve project knowledge, organize it, and make it useful in future work. They work with your existing documents, decisions, and procedures.

## Skills

| Skill | Purpose |
| --- | --- |
| [context-preserve](skills/context-preserve/SKILL.md) | Preserve decisions and findings from sessions or supplied sources, including their rationale and evidence. |
| [context-review-sessions](skills/context-review-sessions/SKILL.md) | Process pending sessions through context-preserve and record completed reviews. |
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

## Optional Codex hooks

The hooks remind the agent about the available skills at session startup and register sessions for later review with `context-review-sessions`. Registration saves session metadata in `.context/sessions.log`; it does not read transcripts or run reviews automatically.

To install in a project:

1. Clone or download this repository and copy `integrations/codex/.codex/` into your project's root. Merge with any existing `.codex/` configuration, preserving unrelated hooks.
2. Ensure Git and Python 3 are on `PATH`: `python3` on Linux/macOS, or `python` and PowerShell on Windows.
3. Add `.context/sessions.log` to the project's `.gitignore`.
4. Use `/hooks` in Codex to review and trust the project hooks.

Install `context-review-sessions` and `context-preserve` to process registered sessions. See the [Codex integration](integrations/codex/README.md) for details.
