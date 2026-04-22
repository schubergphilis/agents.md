# CI/CD

> Part of: [`terraform`](../SKILL.md) skill.
> Purpose: CI pipeline shape and release automation.

## Minimum pipeline for a module

Every module should ship these workflows (or their equivalent on GitLab CI / Azure DevOps / etc.):

1. **PR validation** — title format (conventional commits), required labels.
2. **Terraform validation** — fmt check, tflint, validate per example, `terraform test`, terraform-docs injection, checkov scan.
3. **Label sync** — keep repo labels in sync with the standard set.
4. **Release drafter** — maintain a draft release note on every merge.
5. **Changelog update** — write CHANGELOG.md on publish.

Factor these into **reusable workflows** rather than copy-pasting per repo. A central repo (e.g. `org/github-workflows`) owns the canonical set; module repos invoke them via `workflow_call` or copy with a `DO NOT CHANGE THIS FILE DIRECTLY` header plus a sync process.

## GitHub Actions shape

```yaml
# .github/workflows/terraform-validation.yml
name: terraform

on:
  pull_request:

permissions:
  contents: write
  pull-requests: write

env:
  TF_IN_AUTOMATION: 1

jobs:
  fmt-lint-validate-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: hashicorp/setup-terraform@v3

      - uses: terraform-linters/setup-tflint@v4
        with:
          github_token: ${{ github.token }}

      - name: terraform fmt
        run: terraform fmt -check -recursive

      - name: tflint
        run: |
          tflint --format compact
          for d in examples/*/; do
            tflint --chdir="$d" --format compact
          done

      - name: terraform validate (per example)
        run: |
          for d in examples/*/; do
            terraform -chdir="$d" init -backend=false
            terraform -chdir="$d" validate -no-color
          done

      - name: terraform test
        run: |
          terraform init
          terraform test

  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.head.ref }}
      - uses: terraform-docs/gh-actions@v1.3.0
        with:
          args: --sort-by required
          git-commit-message: "docs(readme): update module usage"
          git-push: true
          output-file: README.md
          output-method: inject
          working-dir: .
        continue-on-error: true

  checkov:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: bridgecrewio/checkov-action@v12
        with:
          directory: "/"
          framework: terraform
          output_format: sarif
          quiet: true
          skip_path: "examples/"
```

## Conventional commits

Enforce PR title format via `amannn/action-semantic-pull-request@v5`. Allowed types:

- `feat` / `feature` — minor bump
- `fix` / `bug` — patch bump
- `breaking` — major bump
- `docs` / `documentation` — patch bump
- `chore` — patch bump
- `security` — patch bump
- `enhancement` — minor bump

Enforce a label on each PR from the same set so `release-drafter` can categorise.

## release-drafter

```yaml
# .github/release-drafter-config.yaml
name-template: "v$RESOLVED_VERSION"
tag-template: "v$RESOLVED_VERSION"
categories:
  - title: ":boom: Breaking Changes"
    labels: [breaking]
  - title: ":rocket: Features"
    labels: [enhancement, feature]
  - title: ":bug: Bug Fixes"
    labels: [bug, fix]
  - title: ":lock: Security"
    labels: [security]
  - title: ":memo: Documentation"
    labels: [documentation, docs]
  - title: ":wrench: Maintenance"
    labels: [chore]
version-resolver:
  major:
    labels: [breaking]
  minor:
    labels: [enhancement, feature]
  patch:
    labels: [bug, fix, security, documentation, docs, chore]
  default: patch
```

Publish draft releases manually — don't auto-publish on merge unless you have a high-confidence release gate.

## Cost optimization

- **Use the smallest runner** that works. Most Terraform module CI fits on `ubuntu-latest`.
- **Cache `terraform init` downloads** when CI runs the same modules repeatedly.
- **Skip unchanged paths** on monorepos via `paths:` / `dorny/paths-filter`.
- **Fan-in status checks** rather than requiring every job individually — faster feedback.

## Automated cleanup

For repos that create real cloud resources in CI:

- Tag every resource with `CI=true, CI-Run=${{ github.run_id }}`.
- Scheduled cleanup workflow that deletes tagged resources older than N hours.
- Budget alarms on the CI account.

## CI anti-patterns

- **`continue-on-error: true`** on a validation step — silently passes broken PRs. Use only on the `terraform-docs` auto-commit step (which can fail for fork PRs).
- **Using `actions/checkout@master`** or `@v1` / `@v2` / `@v3` — mutable or older. Pin to `@v4` or later, or SHA.
- **`hashicorp/setup-terraform@v2`** — `@v3` is current.
- **Running `terraform apply` on PRs** against real infra without sandboxing — costs money and risks real resources.
- **Committing `.terraform/` or `*.tfstate`** — never. State belongs in a backend; `.terraform/` is build output.
- **Ignoring checkov findings without `# checkov:skip=RULE_ID`** with a rationale comment nearby.

## Shared workflow approach

For an org with many modules, factor CI into a central `org/terraform-workflows` repo:

```yaml
# in a module repo: .github/workflows/terraform.yml
name: terraform

on:
  pull_request:

jobs:
  terraform:
    uses: org/terraform-workflows/.github/workflows/terraform.yml@v1
    with:
      examples: "examples/*"
```

Benefits:

- One place to update the pipeline.
- Consistent across the org.
- Module repos only own module code, not CI plumbing.

If your org uses a `DO NOT CHANGE THIS FILE DIRECTLY` copy-paste model instead of `workflow_call`, that works too — but you need a sync process to keep module repos current.

## Action pinning

| Pin style | When OK |
|---|---|
| SHA (`@abc123...40 chars`) | Always. Safest. |
| Exact tag (`@v1.3.0`) | Acceptable for trusted publishers. |
| Minor (`@v1.3`) | Acceptable for trusted publishers. |
| Major (`@v1`) | Acceptable for trusted publishers only. Reject for unknown publishers. |
| Branch (`@main`, `@master`) | **Never.** Mutable reference. |

"Trusted" typically means `actions/*`, `github/*`, `hashicorp/*`, plus a short list of widely-audited community publishers. For any action from an unaudited publisher, SHA-pin or replace.
