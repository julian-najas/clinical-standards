# clinical-standards

Repositorio canonico para seguridad, reproducibilidad y gobierno clinico.

## Composite Actions

### actions/audit-pack
Instala herramientas, ejecuta checks y publica artifacts con logs y salidas.

Entradas principales:
- `install-command`
- `lint-command`
- `typecheck-command`
- `test-command`
- `artifact-name`

### actions/compose-healthcheck
Levanta `docker compose`, espera endpoint de salud, captura logs en fallo y ejecuta `down -v` siempre.

Entradas principales:
- `compose-file`
- `project-directory`
- `health-url`
- `timeout-seconds`
- `artifact-name`

### actions/python-cache
Estandariza setup de Python + cache de dependencias en GitHub Actions.

Entradas principales:
- `python-version`
- `cache`
- `cache-dependency-path`
- `install-command`

## Workflows reutilizables
- `.github/workflows/audit.yml`
- `.github/workflows/repro.yml`
- `.github/workflows/infra-policy.yml`