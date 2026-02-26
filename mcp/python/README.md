# clinical-mcp: Runtime MCP para Clinical Standards

Este paquete implementa el runtime MCP para sistemas clínicos multiagente, con validación de contratos, telemetría y supply chain seguro.

## Instalación

```bash
pip install clinical-mcp
```
# clinical-mcp (runtime)

Hybrid, orchestrator-centric MCP runtime for clinical-grade multi-agent systems:
- **Sync deterministic core** (source of truth)
- **Async outbox side-effects** (notifications, reporting, integrations)
- **Structured eventlog** + **runbook**
- **PII guardrails** (refuse to emit)
- **JSON Schemas + CI validation + OPA enforcement**

## Install (PyPI)

```bash
pip install clinical-mcp
```

## Install (monorepo source-of-truth)

```bash
python -m pip install -e mcp/python
```

## Run demo (monorepo)

```bash
make mcp.install
make mcp.demo
```

Artifacts (default):

- artifacts/mcp/events.jsonl
- artifacts/mcp/run.json
- artifacts/mcp/outbox.sqlite3

## Verify supply chain (release assets)

Each runtime release publishes:

- *.whl, *.tar.gz
- *.sig, *.pem (cosign keyless signatures)
- GitHub provenance attestations (build provenance)
- SBOM (mcp-runtime.sbom.spdx.json)

### 1) Verify cosign signature (blob)

Download the wheel + signature + certificate from the GitHub release assets, then:

```bash
cosign verify-blob \
  --certificate clinical_mcp-<VERSION>-py3-none-any.whl.pem \
  --signature clinical_mcp-<VERSION>-py3-none-any.whl.sig \
  clinical_mcp-<VERSION>-py3-none-any.whl
```

### 2) Verify provenance (GitHub attestations)

For each release tag, GitHub publishes build provenance attestations for dist/*.
Verify via GitHub UI (Release → Attestations) or tu tooling de auditoría.

## Policy: NO PII in events

Events/runbooks must not contain PII (emails, phones, national IDs, names).
Use internal references only (patient_ref, invoice_ref, etc.).
Enforced by:

- runtime guardrails
- CI regex checks
- OPA policies (policies/clinical/events.rego)
## Licencia

MIT
