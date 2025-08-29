# schubergphilis/agents.md 🤖

A community catalog of AGENTS.md files that capture the Schuberg way of working. Use this repository to author, review, and share high-quality agent instructions that encode our standards for setup, code style, testing, commits, and operational excellence.

AGENTS.md is intended to be read by coding agents and humans alike. Keep it precise, testable, and unambiguous.

--------------------------------------------------------------------------------

🎯 Repository goals

- Provide a canonical AGENTS.md template and examples.
- Enforce consistency via linting, link checking, and schema validation.
- Make it easy to discover and reuse AGENTS.md across teams, stacks, and domains.

--------------------------------------------------------------------------------

🗂️ Scope and structure

- Each AGENTS.md is a single self-contained file with the sections below.
- Organize files by domain and technology:
  - catalog/<domain>/<technology>/AGENTS.md (e.g., catalog/platform/terraform/AGENTS.md)
  - catalog/app/<language>/<framework>/AGENTS.md (e.g., catalog/app/python/fastapi/AGENTS.md)
  - catalog/data/<tooling>/AGENTS.md (e.g., catalog/data/dbt/AGENTS.md)
- Prefer smaller, composable AGENTS.md documents over one-size-fits-all. Reference other AGENTS.md where useful.
- Include a short README.md alongside complex AGENTS.md when extra context is necessary.

--------------------------------------------------------------------------------

✍️ Authoring standards (Schuberg way of working)

- Be explicit: prefer “Do X. Do not do Y.” over vague recommendations.
- Be testable: include commands to verify outcomes and acceptance criteria for agents.
- Be secure by default: least privilege, no secrets in code or history, scanners enabled.
- Be operable: logging, metrics, health checks, alerts, and runbooks if relevant.
- Be maintainable: simple over clever; document tradeoffs; avoid snowflakes.
- Be cost-aware and performance-conscious; call out hotspots and limits.
- Be deterministic: pin versions where feasible; define reproducible setups.

--------------------------------------------------------------------------------

📄 AGENTS.md template (copy and adapt)

Use this exact section order and headings. Keep sentences short and imperative. Replace placeholders.

````markdown
---
title: <Short name, e.g., "Terraform Modules (Schuberg Standard)">
version: 1.0.0
owners:
  - <team-or-alias>
last_updated: YYYY-MM-DD
applies_to:
  - <domains, stacks, or repos this targets>
tags:
  - <keywords>
---

# Purpose
- What this AGENTS.md covers in 2–4 bullets.
- What it explicitly does not cover.

# Setup Commands
- Prerequisites:
  - <tools and minimum versions, e.g., "Node >= 20", "Python >= 3.11", "Terraform >= 1.7">
  - <system packages if any>
- Install:
  - <commands to install dependencies>
- Build:
  - <commands to build or compile if relevant>
- Environment:
  - <required environment variables (use placeholders, never real secrets)>

# Code Style
- Language and framework standards:
  - <formatters (e.g., Prettier, Black, gofmt) and configs>
  - <linters (e.g., ESLint, Ruff, golangci-lint) and strictness>
  - <design patterns or folder structures to enforce>
- Documentation:
  - <docstrings, README expectations, ADRs if applicable>
- Security:
  - <secure defaults, dependency pinning, denied patterns>

# Testing
- How to run:
  - <unit, integration, e2e commands>
- Coverage:
  - <minimum thresholds and how to enforce>
- Static checks:
  - <lint, type-check, policy checks>
- Acceptance criteria:
  - <objective checks an agent can verify post-change>

# Commit Guidelines
- Format:
  - Use Conventional Commits: feat|fix|docs|test|chore|refactor|perf|build|ci(scope): summary
  - Examples:
    - feat(api): add pagination to list endpoints
    - fix(ci): pin actions/setup-node to v4
- Branching:
  - <branch naming convention>
- Reviews:
  - <review requirements and CODEOWNERS expectations>
- Change management:
  - <changelog, release notes, semantic versioning>

# Custom Notes
- Security:
  - <secret handling, SCA/DAST/SAST expectations, SBOM, license checks>
- Performance and cost:
  - <benchmarks, limits, tips to reduce compute or egress>
- Operability:
  - <logging, metrics, tracing, runbooks>
- Pitfalls:
  - <common mistakes to avoid>
- References:
  - <links to docs, standards, templates>

# Do and Don’ts (Quick Reference)
- Do: <short imperative rule>
- Don’t: <short imperative rule>
````

--------------------------------------------------------------------------------

🚀 Quick start

- Pick an existing AGENTS.md in catalog that’s closest to your use case.
- Copy the template above and adapt minimally. Keep sections and headings intact.
- Link to other AGENTS.md for shared expectations rather than duplicating content.

--------------------------------------------------------------------------------

🛠️ Setup commands (repository tooling)

This repository provides a minimal toolchain to lint, test, and validate AGENTS.md files.

📦 Prerequisites
- Node.js 20+
- npm 9+ or pnpm 9+
- Optional: Docker (for isolated runs)

📥 Install
- npm ci

🧰 Useful commands
- npm run lint
  - Runs markdownlint and Prettier check on all markdown.
- npm run links
  - Checks for broken links within AGENTS.md files.
- npm test
  - Runs all checks (lint + links + schema validation).
- npm run fix
  - Applies Prettier and autofixes markdownlint issues where possible.
- Docker (optional)
  - docker build -t agents-md . && docker run --rm -v "$PWD":/work agents-md npm test

Note: If you do not use Node, you can replicate these steps with pre-commit, mdformat, and markdown-link-check or lychee. The principle is the same: format, lint, link-check, and validate structure.

--------------------------------------------------------------------------------

🎨 Code style for AGENTS.md

- Formatting
  - Wrap lines at ~100 columns.
  - Use ATX headings (#, ##, ###). Keep the section order from the template.
  - Prefer bullet points over long paragraphs.
  - Use fenced code blocks for commands; mark language where possible.
- Language
  - Imperative, concise sentences aimed at agents.
  - Avoid ambiguous terms (“should”, “try to”). Prefer “must”, “do not”.
- Content
  - Include exact commands and acceptance criteria agents can verify.
  - Keep security-sensitive details out; use placeholders and references.
- Cross-referencing
  - Use relative links for in-repo references.
  - Prefer stable external URLs; avoid volatile links.

--------------------------------------------------------------------------------

✅ Testing

- Linting
  - Ensure markdownlint passes with the repo rules.
  - Ensure Prettier produces no diffs (npm run lint).
- Link checking
  - Ensure all internal and external links resolve (npm run links).
- Structure validation
  - Each AGENTS.md must contain the required headings:
    - Purpose
    - Setup Commands
    - Code Style
    - Testing
    - Commit Guidelines
    - Custom Notes
  - The YAML front matter must include: title, version, owners, last_updated, applies_to, tags.
- Manual spot checks
  - Commands under Setup Commands and Testing should run or be realistically runnable.
  - Acceptance criteria should be objective and verifiable.

--------------------------------------------------------------------------------

📝 Commit guidelines

- Conventional Commits required, examples:
  - feat(catalog/terraform): add standard module scaffolding AGENTS.md
  - fix(catalog/python): correct pytest coverage command
  - docs(readme): clarify contribution flow
  - chore(ci): enable markdown link checker
- Branch naming
  - <type>/<short-topic>, e.g., feat/terraform-modules-v1
- Pull requests
  - Link related issues.
  - Include a brief “Why” and “How” description.
  - Pass all CI checks (lint, links, schema).
  - Get review from CODEOWNERS of the touched area.
- Changelog
  - Changes to templates or global rules should be noted in CHANGELOG.md and bump version fields in the affected AGENTS.md.

--------------------------------------------------------------------------------

🧩 Custom notes (security, performance, governance)

- Security
  - Do not commit secrets. Use placeholders and secret managers.
  - Prefer pinned versions and lockfiles in examples.
  - Include SCA/SAST expectations when relevant; reference internal policies via stable links.
- Performance and cost
  - Highlight known expensive operations; include tips to reduce run time or egress.
  - Prefer incremental or cached workflows in CI examples.
- Governance
  - Use CODEOWNERS to require review for each catalog area.
  - Mark deprecated AGENTS.md with front matter deprecated: true and point to replacements.
- Licensing
  - Keep examples license-compatible and attribute external sources.
  - Follow repository LICENSE once defined.

--------------------------------------------------------------------------------

🤝 Contributing

- Add a new AGENTS.md under catalog/<area>/... following the template.
- Run npm test and fix any issues.
- Open a PR with a clear summary and rationale.
- Expect review on clarity, testability, security posture, and alignment with the Schuberg way of working.

--------------------------------------------------------------------------------

❓ Frequently asked questions

- Why YAML front matter?
  - Enables indexing, discovery, and automated validation.
- Can I merge sections?
  - No. Keep the canonical headings for agents to parse reliably. You can add subheadings if needed.
- Can I reference internal systems?
  - Yes, but use stable URLs and do not reveal confidential details. Prefer documented interfaces over screenshots.

--------------------------------------------------------------------------------

🧪 Minimal example

````markdown
---
title: Python Service (Schuberg Standard)
version: 1.0.0
owners:
  - team-app-platform
last_updated: 2025-08-29
applies_to:
  - app/python/fastapi
tags:
  - python
  - fastapi
  - cicd
---

# Purpose
- Standardize how Python services are built, tested, and delivered.
- Excludes data science notebooks and monoliths.

# Setup Commands
- Prerequisites:
  - Python >= 3.11, pipx, uv
- Install:
  - uv sync
- Build:
  - uv build
- Environment:
  - Export required env vars with placeholders (e.g., DB_URL, SECRET_API_KEY=<from secret manager>)

# Code Style
- Use Ruff (lint) and Black (format) with pyproject.toml pinned.
- Type hints required; run mypy --strict.
- Package layout: src/<pkg> with tests/ alongside.
- Security: bandit -r src; deny eval/exec and unsafe YAML loaders.

# Testing
- Unit: pytest -q
- Coverage: pytest --cov=src --cov-report=term-missing --cov-fail-under=85
- Static: ruff check . && mypy --strict
- Acceptance: Service starts on :8080; /healthz returns 200 in <1s.

# Commit Guidelines
- Conventional Commits; semantic versioning in project.
- PRs require 1 CODEOWNER review; CI must pass.

# Custom Notes
- Performance: prefer uvicorn workers = CPU cores; enable keep-alive.
- Operability: log JSON; include /metrics (Prometheus) and /healthz.
- References: FastAPI docs, internal platform runtime guide.
````

--------------------------------------------------------------------------------

🙏 Acknowledgements

- Inspired by industry patterns for “docs-as-instructions” and agent-safe authoring.
- Contributions welcome; keep it practical, secure, and automatable.
