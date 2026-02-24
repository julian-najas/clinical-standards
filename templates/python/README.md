# Python Template

Plantilla base para que un repo nuevo nazca en modo "empresa-grade" sin pensar.

## Incluye
- `.env.example`
- `Makefile` con `make up`, `make test`, `make audit`
- `docker-compose.yml` (base)
- `docker-compose.dev.yml` (overlay dev)
- `docker-compose.ci.yml` (overlay ci)
- `docs/runbook.md`
- baseline de seguridad (`CODEOWNERS`, `dependabot.yml`, `SECURITY.md`)

## Uso rapido
1. Copia esta carpeta al repo nuevo.
2. Crea `.env` desde `.env.example`.
3. Ajusta `UVICORN_APP`/comando de arranque de tu app.
4. Ejecuta:
   - `make up`
   - `make health`
   - `make audit`

## Minimo esperado para aceptar el repo
- El stack levanta con `make up` sin pasos manuales ocultos.
- `make audit` queda en verde.
- `docs/runbook.md` adaptado al servicio real.
