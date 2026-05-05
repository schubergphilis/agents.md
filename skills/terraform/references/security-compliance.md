# Security and compliance

> Part of: [`terraform`](../SKILL.md) skill.
> Purpose: scanning, secrets, state, and compliance patterns.

## Scanners

Run at least one static security scanner in pre-commit and in CI. Common choices:

| Tool | Strengths | Notes |
|---|---|---|
| **Checkov** | Broad coverage (Terraform, CFN, K8s, Dockerfile). SARIF output. | De-facto standard. |
| **tfsec** | Fast, Terraform-focused. | Now largely merged into Trivy. |
| **Trivy** | One tool for Terraform + containers + filesystems. | Good if you already use it for container scanning. |
| **terrascan** | Policy-as-code via Rego. | Useful when you have OPA experience. |

Pick one and run it in both pre-commit and CI. Running two is usually duplicative.

## Suppressing findings

Suppress individual rules only with an inline comment citing the reason:

```hcl
# checkov:skip=CKV_AWS_18:Logging is centralised at the account level.
resource "aws_s3_bucket" "default" {
  # ...
}
```

Rules:

- Always give a human-readable reason, not just the rule ID.
- Review the suppression when the module changes (does the reason still hold?).
- Never suppress at the repo level with a blanket exclusion.

## Common security issues in modules

- **Public S3/blob storage by default.** Default to private; require explicit opt-in for public.
- **Unencrypted storage.** Default to encrypted; most providers require KMS/CMK for compliance anyway.
- **Wide-open security groups / NSGs.** `0.0.0.0/0` on inbound is almost never the right default.
- **Missing logging.** CloudTrail, VPC flow logs, storage-account diagnostic settings — enable by default.
- **Long-lived access keys.** Prefer OIDC/IAM Roles over access keys. Mark any access key output `sensitive`.
- **TLS < 1.2.** Default to TLS 1.2 minimum; expose knob only to explicitly relax.
- **Missing deletion protection.** RDS, DynamoDB, EKS — callers expect these to be protected by default.

## Secrets handling

### Modules must not accept plaintext secrets

```hcl
# BAD
variable "api_key" {
  type = string
}

# BETTER
variable "api_key_secret_arn" {
  type        = string
  description = "ARN of a Secrets Manager secret holding the API key."
}
```

The caller stores the secret in the secret manager; the module fetches via a data source if it actually needs the value, or just passes the ARN.

### If you must take a plaintext secret

```hcl
variable "api_key" {
  type      = string
  sensitive = true
}
```

- Always `sensitive = true`.
- Default to `null`, not `""`.
- Never log / format / `base64encode` it to stdout.
- Never include it in an output unless the output is also `sensitive = true`.

### Generating secrets in the module

`random_password` is fine for module-generated secrets. Store the result in a secret manager immediately — don't leave it in Terraform state as the primary source:

```hcl
resource "random_password" "db" {
  length  = 32
  special = true
}

resource "aws_secretsmanager_secret_version" "db" {
  secret_id     = aws_secretsmanager_secret.db.id
  secret_string = random_password.db.result
}
```

## State security

- **Remote backend** with state locking (`dynamodb_table` for S3 backend, Azure Storage account with lease-based lock, GCS bucket, or HCP Terraform workspace).
- **Encrypt at rest.** S3 bucket SSE, GCS with CMEK, Azure Storage with CMK.
- **Restrict access.** The state bucket/store has IAM more privileged than anyone else — treat it like a secret vault.
- **Never commit state files.** Add `*.tfstate*` to `.gitignore`.
- **State drift detection.** Scheduled `terraform plan` runs that alert on drift.

## Provider version pinning as a security practice

- Patch updates to providers often fix security issues. A floor-only constraint (`>= 6`) lets callers pick up patches automatically.
- Some providers (e.g. Azurerm, Datadog) need an upper bound at the next major to avoid unreviewed breaking changes.
- **Exact pinning** (`= 6.1.2`) in a module blocks callers from getting security fixes.
- The exact floor number is not important — focus on the constraint shape (floor-only vs floor + ceiling).

## Supply-chain hygiene for modules

- Don't vendor upstream modules. Reference via `schubergphilis/<name>/<provider>` (registry) + a `version = "~> X.Y"` range.
- Never use `source = "github.com/.../repo?ref=<branch>"` — mutable.
- Never use `source = "git::https://.../repo.git"` without a `ref=<tag or SHA>`.
- Lambda code shipped with a module: pin Python `requirements.txt` (`==X.Y.Z`), commit a lockfile for Node (`package-lock.json` / `yarn.lock` / `pnpm-lock.yaml`).
- Action pins: SHA > exact tag > minor > major > never branch (`@main` / `@master`).

## Compliance automation

If you need to prove a control to an auditor:

1. Encode the control as a `validation` or `precondition` block — fail at plan time.
2. Back it with a checkov custom rule that scans for the same pattern — catches it in CI.
3. Document the control ID in a comment next to the check, so the evidence chain is traceable.

Example:

```hcl
resource "aws_s3_bucket_public_access_block" "default" {
  # Security Hub: S3.1 — S3 general purpose buckets should have block public access settings enabled
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
  # ...
}
```

## Defence in depth

A module-level check is cheap but not complete. Pair with:

- Account-level preventive controls (SCPs, Azure Policy).
- Runtime detective controls (CloudTrail, Defender for Cloud, Datadog).
- Regular audit cadence, not just per-PR scans.

Treat module-level checks as the first line, not the only line.
