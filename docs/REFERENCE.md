# Clinical Standards – Public Reference

This document defines the **public API surface** of this repository.

Anything documented here is considered part of the stability contract
as defined in `VERSIONING.md`.

If a component is relied upon by external repositories, it is public.

---

# 1. GitHub Actions

## 1.1 audit-pack (Composite Action)

Location:
```
actions/audit-pack/
```

Purpose:
Run standardized audit checks (install, lint, typecheck, tests) and upload structured artifacts.

Usage:
```yaml
uses: julian-najas/clinical-standards/actions/audit-pack@v1
with:
  python_version: "3.11"
  run-lint: "true"
  run-typecheck: "true"
  run-tests: "true"
  artifacts-dir: "artifacts/audit"
```

### Inputs

| Name              | Default                                                 | Required | Description                              |
| ----------------- | ------------------------------------------------------- | -------- | ---------------------------------------- |
| python_version    | 3.11                                                    | No       | Python version used by setup-python      |
| install-command   | ""                                                      | No       | Optional dependency install command      |
| lint-command      | `ruff check src tests && ruff format --check src tests` | No       | Lint/format command                      |
| typecheck-command | `mypy src`                                              | No       | Typecheck command                        |
| test-command      | `pytest -q`                                             | No       | Test command                             |
| run-lint          | "true"                                                  | No       | Whether to run lint                      |
| run-typecheck     | "true"                                                  | No       | Whether to run typecheck                 |
| run-tests         | "true"                                                  | No       | Whether to run tests                     |
| artifacts-dir     | `artifacts/audit`                                       | No       | Directory where logs/results are written |
| artifact-name     | `audit-artifacts`                                       | No       | Uploaded artifact name                   |
| enable_clinical   | "false"                                                 | No       | Enable clinical OPA tests                |
| opa_version       | ""                                                      | No       | Override OPA version                     |
| opa_sha256        | ""                                                      | No       | Override OPA checksum                    |

### Outputs

| Name           | Description                                 |
| -------------- | ------------------------------------------- |
| overall_failed | "1" if any audit step failed, otherwise "0" |

### Artifacts

Default structure:

```
artifacts/audit/
  install.log
  lint.log
  typecheck.log
  tests.log
  summary.txt
```

These paths are part of the public contract.

---

# 2. Workflows

## 2.1 audit.yml

Location:
```
.github/workflows/audit.yml
```

Purpose:
Standard audit pipeline using audit-pack.

Public expectations:

* Uploads audit artifacts
* Fails if any check fails
* Produces deterministic logs

Consumers may copy or reference this workflow as institutional baseline.

---

## 2.2 repro.yml

Location:
```
.github/workflows/repro.yml
```

Purpose:
Validate reproducibility using docker-compose and health checks.

Public expectations:

* Deterministic environment boot
* Healthcheck validation
* Fails fast on unhealthy state

---

# 3. Policies

Location:
```
policies/
```

Policies are part of the enforcement layer.

Categories may include:

* Conftest / OPA rules
* Docker/Kubernetes baseline restrictions
* Clinical-specific rules (if enabled)

Public guarantees:

* Policy directory structure is stable.
* Rule identifiers remain stable within a major version.
* Breaking tightening requires MAJOR bump.

If `enable_clinical: true`, policies under:

```
policies/clinical/
```

are executed (if present).

---

# 4. Templates

Location:
```
templates/
```

Templates define reproducible project baselines.

Example:
```
templates/python/
```

Public guarantees:

* Documented make targets remain stable.
* Directory structure remains stable within MAJOR.
* Changes affecting build flow require version bump per VERSIONING.md.

---

# 5. Stability Scope

The following are considered stable API within a MAJOR version:

* Action input names
* Action outputs
* Artifact paths and names
* Policy directory paths
* Template entrypoints and documented commands

The following are NOT considered stable unless documented:

* Internal script structure
* Tool patch versions
* Log formatting details (except summary contract)

---

# 6. Consumption Model

Recommended pinning:

Stable major line:

```yaml
uses: julian-najas/clinical-standards/actions/audit-pack@v1
```

Strict reproducibility:

```yaml
uses: julian-najas/clinical-standards/actions/audit-pack@<SHA>
```

---

# 7. Change Governance

Any change affecting components documented here
must follow the rules defined in VERSIONING.md.

If it is not documented here, it is not guaranteed.
