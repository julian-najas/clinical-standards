# Security Policy

## Supported versions
This is a starter template. Define supported versions in your target repository.

## Reporting a vulnerability
1. Do not open public issues with sensitive details.
2. Report privately to the security contact of the target organization.
3. Include impact, reproduction steps, and affected versions.

## Baseline controls for this template
- Secrets stay out of git (`.env` is local only).
- CI must run lint, typecheck, and tests before merge.
- Dependabot updates should remain enabled.
- Container images should be pinned to major/minor tags.
