Scaffold a new skill for sbp-skills.

## Usage

Provide the skill name. All SBP skills use the `sbp-` prefix so they are easy to distinguish from community or personal skills:

```
/new-skill sbp-capacity-planning
/new-skill sbp-decision-record
/new-skill sbp-cost-analysis
```

## What to do

1. Run `sbp-skills dev --skill <name>` to create the scaffold.
2. Edit `skills/<name>/SKILL.md`:
   - **name** — must match directory name
   - **description** — what this skill does and when to use it (50-1024 chars). Be specific so AI tools know when to activate it.
   - **metadata.domain** — what area (platform, security, data-ai, cross-cutting)
   - **metadata.lifecycle** — when it's used (plan, build, run, cross-cutting)
   - **body** — detailed instructions for the agent. Write as if briefing a smart colleague.
3. Validate: `sbp-skills validate skills/<name>`

## Skill writing tips

- Start with "when to use" — help the AI tool decide if this skill is relevant.
- Be specific and actionable — vague instructions produce vague results.
- Include output format — tell the agent exactly how to structure its response.
- For review skills: provide the checklist. For workflow skills: provide the steps.
- Frame for mission-critical: what does a senior SBP engineer check that a generic AI wouldn't?
