# Clinical Standards
Infraestructura de referencia para sistemas multiagente en entornos clínicos privados

## 1. Propósito

Este repositorio define una infraestructura auditable y reproducible para operar sistemas multiagente en clínicas privadas independientes.

- No es un framework.
- No es una demo.
- Es un estándar operativo que integra:
  - Runtime híbrido (determinista + eventos)
  - Contratos formales (JSON Schema versionado)
  - Enforcement (OPA)
  - Supply chain verificable (SLSA + cosign)
  - Gobernanza institucional (CI, registry, versioning)

## 2. Principios de diseño

1. Orchestrator-centric
   - Un único punto de verdad ejecuta el flujo clínico determinista.
2. Sync core + async side-effects
   - Core sincrónico → decisiones clínicas trazables
   - Outbox asíncrono → notificaciones, reporting, integraciones
3. Contrato antes que implementación
   - Eventos y runbooks están definidos por schemas versionados.
   - El contrato es público y estable.
4. PII zero-tolerance
   - Los artefactos nunca contienen datos personales.
   - Solo referencias internas.
5. Monorepo como fuente de verdad
   - Runtime + policies + schemas + ejemplos viven en un único dominio auditable.

## 3. Arquitectura

```
                ┌────────────────────────────┐
                │      Hybrid Orchestrator   │
                │ (Deterministic Core)       │
                └──────────────┬─────────────┘
                               │
                     Structured Events
                               │
                  ┌────────────┴────────────┐
                  │                         │
         events.jsonl               run.json (runbook)
        (append-only log)          (episodio clínico)
                  │
                  │
            ┌─────▼─────┐
            │  Outbox   │  ← Async side-effects
            │ (SQLite)  │
            └─────┬─────┘
                  │
          Notifications / Reporting /
          Integrations / Monitoring
```

## 4. Superficie de contrato

Artefactos públicos:
- artifacts/mcp/events.jsonl
- artifacts/mcp/run.json

Schemas versionados:
- mcp/schemas/v1/
  - event.schema.json
  - run.schema.json

Reglas:
- v1 es estable
- Breaking change → v2 + MAJOR bump
- Schemas publicados en GitHub Pages
- SHA256 registrados en registry

## 5. Enforcement

1. Validación estructural
   - CI valida artefactos contra JSON Schema.
2. Policy enforcement
   - OPA bloquea:
     - emails
     - teléfonos
     - identificadores nacionales
     - patrones sensibles
3. Guardrails runtime
   - El runtime rechaza emisiones con PII.

## 6. Supply Chain

Cada release del runtime incluye:
- wheel + sdist
- SBOM (SPDX)
- Cosign keyless signature
- GitHub build provenance (SLSA)
- Verificación externa posible sin secretos.

## 7. Gobernanza

Incluye:
- VERSIONING.md
- CHANGELOG.md
- CODEOWNERS
- Branch protection
- Self-test CI obligatorio
- Schema registry con hash
- Policies testeadas

El repositorio es auditable como unidad completa.

## 8. Flujo de uso

Clínicas (source-of-truth):
```bash
git clone julian-najas/clinical-standards
cd clinical-standards
make mcp.demo
```
Todo en un entorno reproducible.

Integradores externos:
```bash
pip install clinical-mcp
```
Runtime verificado y firmado.

## 9. Qué NO es

- No es un sistema EHR.
- No es un producto SaaS.
- No es un wrapper de LLMs.
- No es un conjunto de scripts.
- Es infraestructura de referencia.

## 10. Posicionamiento técnico

Clinical Standards define un patrón:

Sistemas multiagente clínicos con trazabilidad determinista, contrato formal y supply chain verificable.

No compite con frameworks de agentes.
Los gobierna.

## Estado

Este repositorio mantiene:
- Contrato estable (v1)
- Runtime híbrido
- Enforcement institucional
- Publicación firmada
- Provenance verificable

Es una base diseñada para permanecer.
