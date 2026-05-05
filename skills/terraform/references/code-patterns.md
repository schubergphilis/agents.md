# Code patterns

> Part of: [`terraform`](../SKILL.md) skill.
> Purpose: HCL code structure, modern features, refactoring patterns.

## Block ordering in a resource

Empty lines separate each group. Within the third group, the identifier comes first, followed by alphabetically sorted other fields, then `tags`.

```hcl
resource "aws_s3_bucket" "default" {
  # 1. Meta-args: count / for_each (kept on top even when written as a block)
  for_each = var.buckets

  # 2. Meta-arg: provider
  provider = aws.replica

  # 3. region, identifier, alphabetically sorted other fields, then tags
  bucket              = each.key
  bucket_prefix       = each.value.prefix
  force_destroy       = each.value.force_destroy
  object_lock_enabled = each.value.object_lock_mode != null
  tags                = var.tags

  # 4. Nested blocks (each separated by empty lines)
  grant {
    id          = each.value.owner_id
    permissions = ["FULL_CONTROL"]
    type        = "CanonicalUser"
  }

  # 5. Meta-arg blocks: depends_on / lifecycle
  lifecycle {
    prevent_destroy = each.value.protected
  }
}
```

## Block ordering in a module

Empty lines separate each group. Within the fourth group, the identifier comes first, followed by alphabetically sorted other fields, then `tags`.

```hcl
module "logging_bucket" {
  # 1. Meta-args: count / for_each
  for_each = var.buckets

  # 2. Meta-args: source / version
  source  = "schubergphilis/s3/aws"
  version = "~> 1.0"

  # 3. Meta-arg: providers
  providers = {
    aws = aws.replica
  }

  # 4. region, identifier, alphabetically sorted other fields, then tags
  name          = each.key
  force_destroy = each.value.force_destroy
  versioning    = true
  tags          = var.tags

  # 5. Nested blocks (each separated by empty lines)
  lifecycle {
    prevent_destroy = true
  }
}
```

## `count` vs `for_each`

Default to `for_each` for nearly everything.

| Situation | Use |
|---|---|
| Toggle a single resource on/off | `count = var.enabled ? 1 : 0` |
| N instances where order matters | `count = length(var.items)` (rare) |
| Multiple instances keyed by name/ID | `for_each = toset(var.items)` or `for_each = var.objects` |
| Resource ID must survive reordering | `for_each` (always) |

`count`-indexed resources have addresses like `aws_s3_bucket.default[0]`; reordering the input list causes Terraform to destroy/recreate. `for_each` maps avoid this.

## Modern Terraform features (≥1.3)

### `optional()` in object types

```hcl
variable "backup" {
  type = object({
    enabled        = optional(bool, false)
    retention_days = optional(number, 30)
    cross_region   = optional(object({
      enabled = bool
      region  = string
    }))
  })
  default = {}
}
```

Callers set only the fields they care about; unset fields use the declared default.

### `moved { }` blocks (≥1.1)

Refactor without destroying state:

```hcl
# moved.tf
moved {
  from = aws_s3_bucket.bucket
  to   = aws_s3_bucket.default
}
```

Use for:

- Renames (fix typos, align with conventions).
- Restructuring into `for_each`/submodules.

### `check { }` blocks (≥1.5)

Post-apply assertions with warnings rather than errors:

```hcl
check "tls_1_2_only" {
  assert {
    condition     = aws_api_gateway_domain_name.default.security_policy == "TLS_1_2"
    error_message = "API Gateway domain must enforce TLS 1.2."
  }
}
```

### `precondition` / `postcondition` (≥1.2)

Fail at plan-time with actionable messages:

```hcl
resource "aws_s3_bucket_logging" "default" {
  lifecycle {
    precondition {
      condition     = var.logging.target_bucket != aws_s3_bucket.default.bucket
      error_message = "Logging target bucket cannot be the bucket itself."
    }
  }
  # …
}
```

Preferred over `null_resource` with `triggers` for invariant checks.

### Provider functions (≥1.8)

```hcl
resource "azurerm_private_endpoint" "default" {
  # …
  private_service_connection {
    name                           = provider::azurerm::normalise_resource_id(var.target_id)
    private_connection_resource_id = var.target_id
  }
}
```

## Version management

The exact floor number is not important — what matters is the **constraint shape**: floor-only for Terraform (no upper bound), and the correct presence or absence of an upper bound for each provider.

### In a module

- `required_version = ">= X.Y"` — floor only, no upper bound on Terraform itself.
- Most providers: floor only (`>= X`), no upper bound.
- Some providers require an upper bound at the next major (`>= X, < (X+1)`). Check the MCAF skill for which providers need this.
- Never `= X.Y.Z` (exact) in a module.
- Avoid `~> X.Y.Z` (patch-tight) — blocks patches.

### In a composition / root

- Same floor pattern, plus a committed `.terraform.lock.hcl`.
- Pin providers more tightly if you must, but in the root not in the module.

## Refactoring patterns

### Splitting a monolithic module

1. Identify orthogonal concerns (networking vs compute vs data).
2. Create new resource modules for each concern.
3. In the old root, replace resources with `module "network" { source = "./modules/network" … }`.
4. Add `moved {}` blocks mapping old addresses to new ones.
5. Run `terraform plan` and verify no resources are destroyed.

### Adding multiplicity after the fact

Going from single to `for_each`:

```hcl
# Before
resource "aws_s3_bucket" "default" { bucket = var.name }

# After
resource "aws_s3_bucket" "default" {
  for_each = toset(var.names)
  bucket   = each.value
}

moved {
  from = aws_s3_bucket.default
  to   = aws_s3_bucket.default["<original_name>"]
}
```

## Locals for clarity

Use `locals` when the expression:

- Appears in more than one place.
- Names a non-obvious invariant (`local.is_production = endswith(var.name, "-prod")`).
- Flattens nested structures for `for_each` (common pattern).

Don't use locals as tag-along variables for single-use intermediate values — just inline the expression.

### Flattening example

```hcl
locals {
  # Expand "one rule → many CIDR blocks" into "many atomic rules"
  ingress_rule_cidrs = flatten([
    for key, rule in var.ingress_rules : [
      for cidr in rule.cidr_blocks : {
        key  = "${key}-${cidr}"
        rule = rule
        cidr = cidr
      }
    ]
  ])
}

resource "aws_vpc_security_group_ingress_rule" "default" {
  for_each = { for r in local.ingress_rule_cidrs : r.key => r }
  # …
}
```

## Error surfaces

Catch errors at the earliest layer:

1. **Type system** — use `optional(...)` with defaults rather than `map(any)`.
2. **Validation blocks** — enumerate valid values, require cross-field invariants.
3. **Preconditions** — for invariants across resources/data sources.
4. **Assertions in `terraform test`** — for derived/conditional logic.
5. **Apply errors** — last resort; should be unreachable for configuration bugs.

## Dependency graph hygiene

- Prefer implicit dependencies via resource references.
- Use `depends_on` only when the dependency cannot be expressed as a reference (e.g. IAM eventual consistency, CloudFormation stack existence).
- Never use `depends_on` to paper over a missing resource reference.

## Deprecated patterns to remove

- `list("a", "b")` / `map("k", "v")` constructor functions → `["a", "b"]` / `{ k = "v" }` literals.
- `aws_s3_bucket_object` → `aws_s3_object`.
- Inline `aws_s3_bucket` sub-blocks (`versioning {}`, `lifecycle_rule {}`) → split resources (`aws_s3_bucket_versioning`, `aws_s3_bucket_lifecycle_configuration`).
- `null_resource` → `terraform_data` (≥1.4).
- `azurerm_function_app` → `azurerm_linux_function_app` / `azurerm_windows_function_app`.
- `aws_lambda_permission` with `function_name = aws_lambda_function.x.function_name` where `.arn` is newer/clearer.
