Scaffold a new domain pack for this repo.

## Usage

Provide the pack name (lowercase-with-hyphens):

```
/new-pack terraform
/new-pack kubernetes
/new-pack data-pipeline
```

## What to do

1. Create `packs/<name>/`.
2. Write the files:
   - **AGENTS.md** — write imperative, verifiable conventions. Under 300 words. Frame for mission-critical: not "best practice" but "what protects the customer"
   - **README.md** — explain what the pack does, which project files indicate it applies, and why it matters
3. Validate: `wc -w packs/<name>/AGENTS.md` reports under 300 words.
4. Add the pack to the packs table in `README.md`.

## Pack writing rules

- Imperative voice: "Run X." not "You should consider running X."
- Every instruction must be verifiable with a command.
- Include an acceptance criteria checklist.
- Keep AGENTS.md under 300 words — if longer, split detailed guidance into a skill.
- CLAUDE.md is optional — only add it if there are Claude Code-specific behaviors.
