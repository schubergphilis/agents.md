# Module patterns

> Part of: [`terraform`](../SKILL.md) skill.
> Purpose: module design and layout best practices.

## Module hierarchy

| Type | When | Scope |
|---|---|---|
| **Resource module** | One logical group of connected resources | VPC + subnets; S3 bucket + policy + encryption |
| **Infrastructure module** | Several resource modules for one purpose | Landing zone for one account |
| **Composition** | Whole deployments, possibly multi-region/account | Org-wide infra |

**Build bottom-up.** Inlining across levels (e.g. a resource module that also creates IAM policies for ten other modules) couples everything and blocks reuse.

## Root files

| File | Purpose | Notes |
|---|---|---|
| `main.tf` | Primary resources | |
| `variables.tf` | All inputs with `type` + `description` | For large modules, split by domain: `variables.network.tf`, `variables.security.tf` |
| `outputs.tf` | All outputs with `description` | |
| `terraform.tf` | `required_version` + `required_providers` | Some codebases call this `versions.tf`; pick `terraform.tf` |
| `locals.tf` | Only if non-empty | |
| `data.tf` | Only if non-empty | |
| `README.md` | Prose + terraform-docs injection | |
| `CHANGELOG.md` | Release history | |
| `LICENSE` | Usually Apache-2.0 for OSS | |

## Variables

### Arg order inside a variable block

```hcl
variable "x" {
  type        = …       # 1. type first
  default     = …       # 2. default (if present)
  description = "…"     # 3. description (always)
  nullable    = false   # 4. nullable (if non-default)
  sensitive   = true    # 5. sensitive (if non-default)
  validation { … }      # 6. validation(s) last
}
```

This order reads well and keeps blocks consistent.

### Typed objects vs flat variables

Prefer complex typed objects:

```hcl
variable "backup" {
  type = object({
    enabled         = optional(bool, false)
    retention_days  = optional(number, 30)
    storage_account = optional(string)
  })
  default     = {}
  description = "Backup configuration."
}
```

over:

```hcl
variable "backup_enabled"        { type = bool   default = false }
variable "backup_retention_days" { type = number default = 30 }
variable "backup_storage_account"{ type = string default = null }
```

The typed object:

- Keeps caller invocation terse (`backup = { enabled = true }`).
- Makes invariants expressible in validation.
- Scales without variable sprawl.

### Validation

Write `validation` for:

- Enumerated values (`contains([...], var.x)`).
- Regex-matching (`can(regex("^…$", var.x))`).
- Cross-field invariants (`var.a != null ? var.b != null : true`).
- Ranges (`var.days >= 7 && var.days <= 30`).

Always give `error_message` a concrete, actionable hint — not just "invalid value".

### Nullable and sensitive

- `nullable = false` when `null` is not a meaningful value. Defaults to `true` which silently admits `null`.
- `sensitive = true` on any secret (API key, password, token, private key). Blocks plan output leakage.
- `default = null` over `default = ""` for "not provided" — lets `var.x == null` work correctly.

### Naming

- `snake_case` everywhere: variable names, output names, local names, resource labels.
- Booleans as statements: `versioning`, `force_destroy`, `bucket_key_encryption_enforced`. Avoid `enable_` / `disable_` prefixes.
- No module-name prefix: in `terraform-aws-mcaf-s3` the variable is `versioning`, not `s3_versioning`.
- No redundant compound outputs: `arn`, not `bucket_arn`.

## Outputs

### Ordering

`id`, `arn`, `name` first (whichever apply to the provider), then outputs ordered by downstream usefulness — not alphabetical.

### Minimum useful surface

Expose the attributes callers actually need. Resist the urge to re-export the whole resource. A common failure mode is:

```hcl
# BAD — leaks everything, including sensitive fields
output "resource" {
  value = aws_kubernetes_cluster.this
}
```

Instead:

```hcl
output "id"   { value = aws_kubernetes_cluster.this.id }
output "name" { value = aws_kubernetes_cluster.this.name }
output "kube_config" {
  value     = aws_kubernetes_cluster.this.kube_config
  sensitive = true
}
```

### Sensitive outputs

Mark credential, token, kubeconfig, connection-string outputs `sensitive = true`. Without it, `terraform plan` prints the value.

## Tags

Reference `var.tags` directly on every taggable resource:

```hcl
resource "aws_s3_bucket" "default" {
  # ...
  tags = var.tags
}
```

Rules:

- `variable "tags" { type = map(string); default = {} }`.
- Reference `var.tags` on every taggable resource. No `local.tags` indirection unless the module genuinely needs to inject extra tags.
- Never hard-code a tag key inside a single resource block.
- Skip `try(var.tags, {})` — useless when the var has a default.

## Resource argument ordering inside a block

Empty lines separate each group:

1. `count` / `for_each` — meta-args first; even when written as a block, keep on top.
2. `provider`.
3. `region`, identifier (`name`, `bucket`, `resource_group_name`, `location`, …), then **alphabetically sorted** other fields, then `tags`.
4. Nested blocks (each separated by empty lines).
5. Meta-argument blocks: `depends_on`, `lifecycle`.

## Module argument ordering inside a block

Empty lines separate each group:

1. `count` / `for_each`.
2. `source`, `version`.
3. `providers`.
4. `region`, identifier (`name`, …), then **alphabetically sorted** other fields, then `tags`.
5. Nested blocks (each separated by empty lines).
6. Meta-argument blocks: `depends_on`, `lifecycle`.

## Resource labels

- Single instance of a resource type in a module → use a canonical label. Common conventions: `"default"` (used by AWS community + anton-babenko style), `"this"` (used by azurerm community).
- **Pick one per organisation and stick with it.** Mixing `"default"` and `"this"` in one repo is noise.
- For additional instances of the same resource type: use a descriptive label (`"logging"`, `"replica"`, `"cmk"`), not `"default2"`.
- With `for_each`/`count`, keep the canonical single label — multiplicity is expressed by the meta-arg.

## Multi-provider orchestration

If a module legitimately needs two providers (e.g. AWS S3 replication between accounts):

```hcl
terraform {
  required_providers {
    aws = {
      source                = "hashicorp/aws"
      version               = ">= 6.0, < 7.0"
      configuration_aliases = [aws.source, aws.destination]
    }
  }
}
```

Callers then pass both providers:

```hcl
module "s3_repl" {
  source = "…"
  providers = {
    aws.source      = aws.us_east_1
    aws.destination = aws.eu_west_1
  }
}
```

Never put `provider "aws" { region = "…" }` inside a reusable module. Provider configuration is the caller's responsibility.

## README

```markdown
# <repo-name>

<one-line purpose>

IMPORTANT: We do not pin modules to versions in our examples. Pin in your own code
so that your infrastructure remains stable.

## <prose sections for non-obvious behaviour — gotchas, security notes, caveats>

<!-- BEGIN_TF_DOCS -->
<!-- injected by terraform-docs via CI; DO NOT EDIT -->
<!-- END_TF_DOCS -->

## Licensing

Apache-2.0. See [LICENSE](LICENSE).
```

- First H1 = repo name.
- Prose sections above the `BEGIN_TF_DOCS` / `END_TF_DOCS` markers, not inside.
- No hand-written `## Usage` blocks with HCL snippets — they rot. Point people to `examples/` instead.
- End with `## Licensing`.

## Anti-patterns to avoid

- Whole-resource outputs (`output "resource" { value = aws_x.this }`) — leak everything.
- Hard-pinned child-module refs (`source = "git::…?ref=v1.2.3"`) inside a reusable module. Propagates version debt outward.
- Two sources of truth for the same field (`var.name` and `var.config.name`).
- Creating a resource group / VPC inside a resource module — caller should own shared infrastructure.
- `provider "aws" { … }` blocks inside a reusable module.
- `try(var.tags, {})` cargo-culted around variables with a default.
- `default = null` on a genuinely required input — contradicts the description.
- Empty `outputs.tf`.
- Missing `sensitive = true` on secrets.
- Floating `:latest` / `:main` image/version defaults — non-idempotent.
- Dead variables, locals, commented-out resources.
- File-naming drift (camelCase, `backend.tf` / `module.tf` misuse).
- Nested ternaries in variable bodies that `optional(field, default)` would eliminate.
- `null_resource` or deprecated resources (`aws_s3_bucket_object`, `azurerm_function_app`) in new code.

## Examples directory

Every module must have `examples/default/`. Add additional `examples/<scenario>/` per major feature branch. Rules:

- Each example is runnable (`terraform init && terraform validate` passes).
- Examples reference the module via relative source (`source = "../../"`) — no `version = …`.
- Each example is linted in CI.
- CI runs `terraform validate` and optionally `tflint` per example.
