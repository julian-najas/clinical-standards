# clinical-standards

Repositorio canonico para seguridad, reproducibilidad y gobierno clinico.

Si es tu primera vez aqui, empieza por `docs/START_HERE.md`.

## Current Version

Stable: v1.0.0  
Branch: main (protected)  
Compatibility: SemVer

## Governance Model

- Motor CI reusable (stable)
- Infra baseline policies (stable)
- Clinical layer (opt-in, evolving)
- All changes require PR + review

## Mapa Rapido
- `/.github/workflows/`: workflows reutilizables canonicos.
- `/actions/`: composite actions para evitar duplicar pasos.
- `/policies/conftest/`: politicas OPA/Conftest para repos infra/GitOps.
- `/policies/clinical/`: overlay de reglas y esquemas clinicos (opt-in).
- `/semgrep/rules/`: reglas de seguridad de dominio clinico.
- `/templates/python/`: plantilla lista para crear nuevos repos.

## Que Usar En Cada Caso
- Quieres gate de calidad/seguridad en un repo app:
  Usa `.github/workflows/audit.yml` + `actions/audit-pack`.
- Quieres test de reproducibilidad docker:
  Usa `.github/workflows/repro.yml` + `actions/compose-healthcheck`.
- Quieres politicas para manifiestos:
  Usa `.github/workflows/infra-policy.yml` + `policies/conftest`.
- Quieres validaciones de consentimiento clinico (opt-in):
  Usa `policies/clinical/` con `enable_clinical: 'true'` en `actions/audit-pack`.
- Quieres estandarizar cache Python:
  Usa `actions/python-cache`.
- Quieres arrancar un repo nuevo:
  Copia `templates/python/` completo.

## Composite Actions

### `actions/audit-pack`
Instala herramientas, ejecuta checks y sube artifacts con logs/resultados.

Entradas principales:
- `install-command`
- `lint-command`
- `typecheck-command`
- `test-command`
- `artifact-name`
- `enable_clinical`

### `actions/compose-healthcheck`
Levanta `docker compose`, espera endpoint de salud, sube logs y ejecuta `down -v` siempre.

Entradas principales:
- `compose-file`
- `project-directory`
- `health-url`
- `timeout-seconds`
- `artifact-name`

### `actions/python-cache`
Estandariza `setup-python` + cache de dependencias y comando de instalacion opcional.

Entradas principales:
- `python-version`
- `cache`
- `cache-dependency-path`
- `install-command`

## Workflows Reutilizables
- `.github/workflows/audit.yml`
- `.github/workflows/repro.yml`
- `.github/workflows/infra-policy.yml`
- `.github/workflows/release.yml`

## Plantilla Recomendada
La base para proyectos nuevos esta en `templates/python/`.

Incluye:
- `.env.example`
- `Makefile` (con `make up/test/audit`)
- `docker-compose.yml` + overlays dev/ci
- `docs/runbook.md`
