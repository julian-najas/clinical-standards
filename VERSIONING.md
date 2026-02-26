## Schema Registry Integrity

All public schemas are indexed in `mcp/schemas/registry.json`.
Each entry includes a SHA256 digest.

Any schema modification requires:
- Regeneration of registry
- Version classification per SemVer
- CI passing registry integrity check
# Versioning Policy

This repository follows **Semantic Versioning (SemVer)**: `MAJOR.MINOR.PATCH`.

Because this is a **standards repository**, the “public API” is not code-only. The public API includes:
- **GitHub Actions** under `actions/**` (inputs, outputs, defaults, behavior, artifact paths)
- **Workflows** under `.github/workflows/**` when designed to be reused/copied as standards
- **Policies** under `policies/**` (OPA/Conftest/Semgrep rules and their enforcement levels)
- **Templates** under `templates/**` (project structure, make targets, expected outputs)


**Contract surface:**
- Cambios en `mcp/schemas/v1/*.json` = MAJOR (rompe consumidores que parsean eventos/runbook).
- Nuevos schemas en `mcp/schemas/v2/` = MINOR (no rompe v1).
If it is relied upon by consumers, it is part of the public contract.

---

## Supported release tags

Consumers should pin using one of:
- `@vMAJOR` (recommended for most repos): e.g. `@v1`
- `@vMAJOR.MINOR.PATCH` (exact SemVer): e.g. `@v1.2.3`
- `@<SHA>` (maximum reproducibility / supply-chain strict)

**Policy:** we maintain a moving `vMAJOR` tag (e.g. `v1`) that always points to the latest compatible release in that major line.

---

## What is considered BREAKING (MAJOR)

A change requires a **MAJOR** bump if it breaks existing consumers that pin within the same major line.

### Actions (`actions/**`)
Breaking examples:
- Rename/remove an input or output.
- Change input meaning, type, accepted values, or default behavior in a way that can change outcomes.
- Change artifact naming conventions or locations **if consumers plausibly depend on them**.
- Remove a step/tool from the audit pack that consumers rely on for baseline compliance.

**Special rule:** tightening checks (making previously passing builds fail) is **breaking** unless it is strictly opt-in.

### Workflows (`.github/workflows/**`)
Breaking examples:
- Rename jobs/steps that consumers reference via `needs`, outputs, or artifact names.
- Change required secrets/permissions.
- Change artifact paths/names in a way that downstream automation depends on.

### Policies (`policies/**`)
Breaking examples:
- Add or tighten a deny rule that can cause existing infrastructure/configs to fail validation by default.
- Change rule IDs/names that downstream tooling references.
- Move policy directories used by consumers.

### Templates (`templates/**`)
Breaking examples:
- Remove or rename standard targets (`make audit`, `make health`, etc.) if documented as guaranteed.
- Change directory layout in a way that breaks referenced commands.

---

## What is MINOR (backwards-compatible feature)

A change requires a **MINOR** bump if it adds capability without breaking existing consumers.

Examples:
- Add a new optional input with a safe default.
- Add a new workflow or policy that is **opt-in**.
- Add additional artifacts while keeping existing ones unchanged.
- Expand documentation and examples.

---

## What is PATCH (bugfix / non-contract changes)

A change requires a **PATCH** bump if it fixes behavior without changing contract.

Examples:
- Fix a script bug while keeping interfaces stable.
- Internal refactors.
- Docs-only changes.
- Pin updates for security that do not change public behavior.

---

## Defaults and “silent breaks”

Defaults are part of the public contract when they affect outcomes.
- Changing a default that changes pass/fail behavior or artifact paths is **at least MINOR**.
- If consumers are likely to rely on the old default, treat it as **MAJOR** or provide compatibility.

**Recommendation:** when changing a default, consider:
1) keeping old behavior available via input,
2) emitting a clear log line indicating the new default,
3) documenting in CHANGELOG with migration notes.

---

## Deprecation policy

We use a two-step deprecation lifecycle:
1) Mark as deprecated in a **MINOR** release (documented in CHANGELOG).
2) Remove in the next **MAJOR** release.

Minimum deprecation window:
- At least one MINOR release cycle.
- If removal impacts widely used actions/workflows, provide a migration guide.

---

## Compatibility guarantees

Within a given `MAJOR` line (e.g. `v1.x.x`), we guarantee:
- Existing action inputs/outputs remain valid.
- Existing artifact names/paths remain stable unless clearly documented and compatible alternatives exist.
- Policy directories and rule identifiers remain stable unless marked deprecated.

---

## Migration notes

All breaking changes MUST include:
- A CHANGELOG entry under “Changed” or “Removed”
- A short “Migration” section describing required consumer updates
# VERSIONING

Policy for `clinical-standards` releases.

## Scheme
- We use Semantic Versioning: `MAJOR.MINOR.PATCH`.
- A release is an immutable Git tag plus a published GitHub Release.
- Consumers should pin to a tag (`@v1.0.0`) or major channel (`@v1`).

## Change classification
- `MAJOR`: breaking changes in reusable workflows, composite actions, or required inputs/outputs.
- `MINOR`: backward-compatible additions (new optional inputs, extra checks, new templates).
- `PATCH`: backward-compatible fixes and documentation corrections.

## Compatibility rules
- Do not remove or rename required inputs/outputs in a minor or patch release.
- Deprecations must be announced in `README.md` before removal.
- Security hotfixes may ship as patch releases with release notes.

## Release process
- Merge to `main` with green CI.
- Create annotated tag `vX.Y.Z` on `main`.
- Publish GitHub Release notes with migration guidance when needed.
