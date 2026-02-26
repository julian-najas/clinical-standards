# Verification Guide (Top-Level)

This repository is designed to be auditable end-to-end:
schemas + runtime + policies + examples in a single monorepo.

## A) Verify schemas
- Schemas are versioned under `mcp/schemas/v1/`
- Published to GitHub Pages under `docs/schemas/v1/`

CI guarantees:
- schema lint (valid Draft 2020-12)
- docs/schema sync (no divergence)
- registry SHA256 integrity (if enabled)

## B) Verify runtime release integrity (GitHub release assets)

1) Download wheel and signature:
- `clinical_mcp-<VERSION>-py3-none-any.whl`
- `clinical_mcp-<VERSION>-py3-none-any.whl.sig`
- `clinical_mcp-<VERSION>-py3-none-any.whl.pem`

2) Verify signature:
```bash
cosign verify-blob \
  --certificate clinical_mcp-<VERSION>-py3-none-any.whl.pem \
  --signature clinical_mcp-<VERSION>-py3-none-any.whl.sig \
  clinical_mcp-<VERSION>-py3-none-any.whl
```

3) Verify provenance:

* GitHub release includes build provenance attestations for `dist/*`.

## C) Verify policies (OPA)

Run policy tests:

```bash
opa test policies/clinical -v
```

## D) Verify runtime artifacts conform to schemas

Generate artifacts (demo):

```bash
make mcp.install
make mcp.demo
```

Validate:

```bash
make mcp.validate
make mcp.opa
```
