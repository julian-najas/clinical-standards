# Changelog

All notable changes to this project are documented in this file.

## [Unreleased]

## [1.1.0] - 2026-02-25

### Changed
- Unified OPA setup through a shared action (`actions/setup-opa`).
- Upgraded and aligned OPA default version to `v1.13.2` across policy workflows.
- Replaced fixed external action SHA usage for `audit-pack` with same-ref local action resolution in reusable workflows.
- Pinned Semgrep engine version in reusable audit workflow (`semgrep_version`, default `1.145.0`).

### Security
- Added checksum verification and retry logic for OPA and Conftest downloads.
- Removed floating references in reusable action wiring and enforced deterministic workflow toolchain behavior.

## [1.0.0] - 2026-02-24

### Added
- Clinical standard baseline (`policies/clinical/standards/v1.0`).