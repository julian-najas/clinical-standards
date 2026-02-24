# VERSIONING

Policy for `clinical-standards` releases.

## Scheme
- We use Semantic Versioning: `MAJOR.MINOR.PATCH`.
- Releases are immutable Git tags only.
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
- Publish release notes with migration guidance when needed.