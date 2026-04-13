Scaffold a new domain pack for sbp-skills.

## Usage

Provide the pack name (lowercase-with-hyphens):

```
/new-pack terraform
/new-pack kubernetes
/new-pack data-pipeline
```

## What to do

1. Run `sbp-skills dev --pack <name>` to create the scaffold.
2. Fill in the generated files:
   - **manifest.toml** — set description (min 50 chars), detection file patterns, and targets
   - **AGENTS.md** — write imperative, verifiable conventions. Under 300 words. Frame for mission-critical: not "best practice" but "what protects the customer"
   - **README.md** — explain what the pack does, what it auto-detects, and why it matters
3. Add detection rules to `detection.toml` if auto-detection is desired.
4. Validate: `sbp-skills validate packs/<name>`
5. Test: run `sbp-skills init` in a project that matches the detection pattern and verify the AGENTS.md content appears.

## Pack writing rules

- Imperative voice: "Run X." not "You should consider running X."
- Every instruction must be verifiable with a command.
- Include an acceptance criteria checklist.
- Keep AGENTS.md under 300 words — if longer, split detailed guidance into a skill.
- CLAUDE.md is optional — only add it if there are Claude Code-specific behaviors.
