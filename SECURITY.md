# Security Policy

This repository defines institutional standards for clinical engineering workflows.
Security is core to its purpose.

---

# Reporting a Vulnerability

If you discover a security vulnerability:

- Do NOT open a public issue.
- Email: security@your-domain.com
- Include:
	- Description
	- Steps to reproduce
	- Impact assessment
	- Suggested remediation (if available)

We will acknowledge within 48 hours.

---

# Scope

Security issues include:

- Supply chain vulnerabilities (GitHub Actions pinning, tool versions)
- Policy bypass vectors
- Artifact tampering
- Logging or data leakage risks
- Misconfiguration allowing secrets exposure

---

# Action Pinning Policy

All third-party GitHub Actions must be pinned to a commit SHA.

Example:
uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683

Floating tags are not allowed.

---

# Responsible Disclosure

We commit to:

- Timely investigation
- Coordinated disclosure
- Patch release with clear advisory
- Credit where appropriate
