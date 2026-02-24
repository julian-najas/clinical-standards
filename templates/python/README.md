# Python Template

Plantilla canonica para que un nuevo repo Python (FastAPI + Postgres + Redis)
nazca correcto desde el primer commit.

## Estructura incluida
- `Dockerfile`
- `docker-compose.yml`
- `docker-compose.dev.yml`
- `docker-compose.ci.yml`
- `Makefile`
- `.env.example`
- `.gitignore`
- `.dockerignore`
- `.editorconfig`
- `.pre-commit-config.yaml`
- `pyproject.toml`
- `src/app/main.py`
- `tests/test_health.py`
- `docs/runbook.md`
- `runbook.md` (alias por compatibilidad)
- `CODEOWNERS`
- `dependabot.yml`
- `SECURITY.md`

## Uso rapido
1. Copia todo `templates/python/*` al nuevo repositorio.
2. Crea `.env` desde `.env.example`.
3. Ejecuta:
   - `make up`
   - `make health`
   - `make audit`

## Criterio de aceptacion
- `make up` levanta API + Postgres + Redis sin pasos ocultos.
- `make health` responde `ok`.
- `make audit` queda en verde.
- `docs/runbook.md` se adapta al dominio real del servicio.

## Notas de seguridad
- No subir `.env` al repositorio.
- Postgres y Redis no se exponen fuera del compose por defecto.
- No usar imagenes `:latest` en repos productivos.
