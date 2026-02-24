# Runbook Operativo

## Objetivo
Este runbook define como operar, diagnosticar y recuperar un servicio clinico estandar
basado en FastAPI + Postgres + Redis usando docker compose.

## 1. Arranque rapido
1. Copiar variables: `cp .env.example .env`
2. Levantar stack: `make up`
3. Validar salud: `make health`
4. Ver logs: `make logs`

## 2. Comandos de operacion
- Estado de servicios: `make ps`
- Baja limpia: `make down`
- Ejecutar tests: `make test`
- Ejecutar gate local: `make audit`

## 3. Incidente: API no responde
1. Revisar estado: `make ps`
2. Revisar logs API: `docker compose logs app --tail=200`
3. Verificar puerto local: `curl -fsS http://127.0.0.1:8000/health`
4. Reiniciar stack: `make down && make up`

## 4. Incidente: fallo de DB o Redis
1. Logs DB: `docker compose logs postgres --tail=200`
2. Logs Redis: `docker compose logs redis --tail=200`
3. Salud DB: `docker compose exec postgres pg_isready -U $$POSTGRES_USER -d $$POSTGRES_DB`
4. Salud Redis: `docker compose exec redis redis-cli ping`
5. Si hay corrupcion local dev: `make down` y borrar volumenes (`-v` ya incluido)

## 5. Incidente: CI roja
1. Ejecutar local: `make audit`
2. Verificar formato/tipado:
   - `make lint`
   - `make format`
   - `make typecheck`
3. Si falla reproducibilidad:
   - `docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build -d`
   - `curl -fsS http://127.0.0.1:8000/health`

## 6. Criterio de salida (Done)
- `make audit` en verde
- `make health` en verde
- Stack levantable con `make up` sin pasos manuales ocultos
- Secretos fuera de git (`.env` local, no versionado)
