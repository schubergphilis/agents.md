# Ideas and Roadmap

Things to build next. Roughly prioritized — top items have the most impact.

## Domain packs to create

These have detection rules ready (commented out in `detection.toml`). Each needs a `manifest.toml`, `AGENTS.md`, and `README.md` under `packs/`.

- **terraform** — mission-critical infrastructure: state management, plan-before-apply, module structure, rollback strategies, drift detection. Auto-detected by `*.tf`.
- **kubernetes** — production-grade k8s: resource limits, health probes, PDB, RBAC, network policies, rollout strategies. Auto-detected by `k8s/*.yaml`, `helm/Chart.yaml`.
- **docker** — container best practices: minimal base images, multi-stage builds, no root, layer caching, security scanning. Auto-detected by `Dockerfile`.
- **github-actions** — CI/CD conventions beyond supply-chain pinning: secret handling, matrix testing, caching, artifact management. Auto-detected by `.github/workflows/*.yml`.

Other packs to consider:
- **ansible** — idempotent playbooks, vault for secrets, role structure
- **data-pipeline** — dbt, Airflow, or Spark conventions for mission-critical data
- **azure/aws** — cloud-specific conventions (IaC patterns, networking, IAM)

## Skills to create

**Planning:**
- **capacity-planning** — sizing, scaling limits, degradation thresholds, load testing guidance
- **decision-record** — capture architectural decisions with context, alternatives considered, and trade-offs (ADR format)
- **change-impact-analysis** — trace the impact of a change across systems, teams, and processes

**Building:**
- **api-design** — API design for resilience: backward compatibility, versioning, error contracts, rate limiting, idempotency
- **database-migration** — safe migration patterns: backward-compatible changes, blue-green schemas, rollback strategies

**Running:**
- **cost-analysis** — cloud cost review, right-sizing, reserved capacity recommendations

**Cross-cutting:**
- **compliance-evidence** — generate evidence artifacts for ISO 27001/9001 audits: control mappings, change records, access reviews
- **knowledge-transfer** — document decisions and context for handover between teams or during offboarding
- **onboarding-guide** — generate a project-specific onboarding document from the codebase for new joiners

## CLI improvements

- **Remote repo support** — `sbp-skills init` should `git clone` from a configured remote URL, not just use local paths. Needed for real deployment.
- **`sbp-skills browse`** — interactive picker showing available packs/skills with descriptions. Simple numbered list, not TUI.
- **Copilot rendering** — write to `.github/copilot-instructions.md` alongside AGENTS.md for GitHub Copilot users.
- **OpenCode rendering** — verify OpenCode reads AGENTS.md and document any tool-specific setup.
- **`sbp-skills status`** — show what's installed, what's outdated, what new content is available since last update.
- **Windows support** — test install.ps1, verify paths work on Windows. Python is cross-platform but paths and symlinks need testing.

## Content quality

- **Test with real projects** — run `sbp-skills init` on actual SBP projects and evaluate whether the agent's behavior noticeably improves. Collect feedback from engineers.
- **Baseline word count discipline** — currently 297 words. As we add more, resist the urge to grow it. The baseline should stay tight. If something needs depth, make it a skill.
- **Pack word count audit** — keep each pack under 300 words. If conventions need more detail, split into pack (summary) + skill (depth).
- **Command effectiveness** — test each command in real conversations. Does `/review` actually catch things? Does `/challenge` ask useful questions? Iterate on the prompts based on real use.

## Distribution

- **Host the repo** — push to GitHub/GitLab so `install.sh` and `sbp-skills update` work for real.
- **Versioning** — tag releases so teams can pin to a version and update deliberately.
- **Changelog** — track what changes between versions so teams know what they're getting on update.

## Longer-term ideas

- **Metrics** — track which skills and commands are actually used. What do engineers reach for? What collects dust?
- **Team-specific packs** — allow teams to maintain their own packs in a separate repo that sbp-skills can pull from alongside the central one.
- **Feedback loop** — let engineers flag when the agent gives bad advice or misses something. Feed that back into improving the content.
- **Multi-language support** — some SBP teams may work in Dutch. Consider whether any content should be localized.
