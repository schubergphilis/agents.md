# Quick reference

> Part of: [`terraform`](../SKILL.md) skill.
> Purpose: cheat sheets for rapid consultation.

## Command cheat sheet

Works with both `terraform` and `tofu`.

```bash
# Format + lint
terraform fmt -check -recursive
tflint --format compact
tflint --chdir=examples/default

# Validate + plan per example
for d in examples/*/; do
  terraform -chdir="$d" init -backend=false
  terraform -chdir="$d" validate -no-color
done

# Native tests
terraform init                   # fetch providers
terraform test                   # run all .tftest.hcl
terraform test -verbose
terraform test -filter=tests/main.tftest.hcl

# Pre-commit
pre-commit install                # install git hook
pre-commit run -a                 # run all hooks on all files

# Docs
terraform-docs . --sort-by required
terraform-docs . --output-file README.md --output-method inject

# Security
checkov -d .
trivy config .

# State
terraform state list
terraform state show <addr>
terraform state mv <from> <to>
terraform state rm <addr>

# Migrations
# Prefer `moved {}` blocks over `terraform state mv` for reproducibility.
```

## Decision flowchart

```
Start: new module
├── Is it a single resource group (VPC, bucket, cluster)?
│   └── Resource module
├── Is it a set of resource modules for one purpose?
│   └── Infrastructure module (calls resource modules)
└── Is it an entire environment/account?
    └── Composition (calls infrastructure modules)

Start: new variable
├── Is the value genuinely optional or has a sensible default?
│   └── default = <something>
├── Is null a meaningful input?
│   └── default = null
├── Is null NOT meaningful?
│   └── nullable = false (no default, required)
├── Is it a secret?
│   └── sensitive = true
├── Are valid values enumerable?
│   └── validation { condition = contains([...], var.x) }
└── Has cross-field invariants?
    └── validation { condition = … complex … }

Start: new resource field
├── Same for all calls?
│   └── Hard-code
├── Differs per call, N possible values?
│   └── variable with validation
├── Differs per call, derived from another variable?
│   └── local
└── Differs per caller, complex shape?
    └── typed object variable with optional(…)

Start: multiplicity
├── One instance, always?
│   └── No count/for_each
├── One or zero?
│   └── count = var.enabled ? 1 : 0
├── Stable keys, known at plan time?
│   └── for_each = toset(var.items) or for_each = var.objects
└── Positional, order-sensitive?
    └── count = length(…) — rare, prefer for_each
```

## Version-specific guidance

| Version | Features |
|---|---|
| 0.12 | HCL 2, `for`/`dynamic` — floor for anything current. |
| 0.13 | Provider source addresses in `required_providers`. |
| 1.0 | Stability guarantee; safe floor. |
| 1.1 | `moved {}` blocks. |
| 1.2 | `precondition` / `postcondition`. |
| 1.3 | `optional(field, default)` in object types. |
| 1.4 | `terraform_data` replaces `null_resource`. |
| 1.5 | `check {}` blocks; `import {}` block. |
| 1.6 | Native `terraform test` (alpha ≥1.6, mature ≥1.7). |
| 1.7 | `removed {}` block for intentional un-management. |
| 1.8 | Provider functions (`provider::<ns>::<fn>()`). |
| 1.9+ | Modern baseline — recommended floor for new code. |

If your module is still on `>= 0.13`, you're blocked from every feature above it. Bump on next touch.

## Troubleshooting

### `terraform validate` passes but `terraform plan` errors

Usually a reference to an attribute that doesn't exist on the resource you referenced (most common: `.id` vs `.name` vs `.arn`). `validate` doesn't evaluate expressions that depend on actual resource schemas.

### `for_each` producing "may only be given a map or a set of strings"

You have `for_each = var.x` where `var.x` is `list(string)`. Convert with `toset(var.x)`.

### "Cycle" errors

Two resources / modules reference each other. Usually solved by:

- Splitting the offending attribute into a data source.
- Using `depends_on` where a reference can't work.
- Extracting a shared local that both consume (breaks the cycle in the graph).

### `mock_provider` in tests is returning `null` for fields I mocked

Did you use `mock_data` for a data source (correct) where the resource is actually a resource? Use `mock_resource` (provider-level) or `override_resource` (run-level) instead.

### Provider version conflict on `terraform init`

Multiple child modules demand incompatible version ranges. Look at the union in `terraform providers`. Often fixed by widening one module's range to include the other's.

### `moved {}` block ignored

`moved` only works within the same module. Cross-module moves need `terraform state mv` or a refactor that routes state through the correct module boundary.

## Migration paths

### From `count` to `for_each`

```hcl
# Before
resource "aws_s3_bucket" "default" { bucket = var.name }

# After
resource "aws_s3_bucket" "default" {
  for_each = toset([var.name])
  bucket   = each.value
}

moved {
  from = aws_s3_bucket.default
  to   = aws_s3_bucket.default[var.name]
}
```

### From `versions.tf` to `terraform.tf`

```bash
git mv versions.tf terraform.tf
# commit + push
```

Pure rename; CI picks it up. No state change.

### From deprecated `aws_s3_bucket_object` to `aws_s3_object`

```hcl
resource "aws_s3_object" "default" { … }

moved {
  from = aws_s3_bucket_object.default
  to   = aws_s3_object.default
}
```

### From `null_resource` to `terraform_data`

```hcl
resource "terraform_data" "default" {
  triggers_replace = [var.version]
}

moved {
  from = null_resource.default
  to   = terraform_data.default
}
```

Requires `required_version = ">= 1.4"`.

## Common `validation` patterns

```hcl
# Enumerated
validation {
  condition     = contains(["small", "medium", "large"], var.size)
  error_message = "size must be small, medium, or large."
}

# Regex (name prefix, CIDR, ARN shape)
validation {
  condition     = can(regex("^[a-z0-9-]+$", var.name))
  error_message = "name must be lowercase letters, digits, and hyphens only."
}

# Cross-field
validation {
  condition     = var.name == null || var.name_prefix == null
  error_message = "Specify name or name_prefix, not both."
}

# List non-empty
validation {
  condition     = length(var.ids) > 0
  error_message = "At least one id is required."
}

# Numeric range
validation {
  condition     = var.retention_days >= 7 && var.retention_days <= 35
  error_message = "retention_days must be between 7 and 35."
}

# Nested object invariant
validation {
  condition = alltrue([
    for r in var.rules : r.from_port <= r.to_port
  ])
  error_message = "Each rule must have from_port ≤ to_port."
}
```
