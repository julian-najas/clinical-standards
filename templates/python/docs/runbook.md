# Runbook Operativo

## 1. Objetivo
Operacion base para servicios Python con FastAPI + Postgres + Redis.

## 2. Arranque rapido
1. Crear entorno local: `cp .env.example .env`
2. Levantar stack: `make up`
3. Validar salud: `make health`
4. Ver logs: `make logs`

## 3. Operacion diaria
- Estado: `make ps`
- Shell de app: `make sh`
- Pruebas: `make test`
- Gate completo: `make audit`
- Apagar y limpiar: `make down`

## 4. Incidente: API no responde
1. `make ps`
2. `make logs`
3. `curl -fsS http://127.0.0.1:8000/health`
4. `make restart`

## 5. Incidente: fallo de Postgres/Redis
1. `docker compose logs postgres --tail=200`
2. `docker compose logs redis --tail=200`
3. `docker compose exec postgres pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB"`
4. `docker compose exec redis redis-cli ping`

## 6. Incidente: CI en rojo
1. `make audit`
2. Reintentar en limpio: `make clean && make up && make audit`
3. Confirmar que `.env` no contiene secretos reales para CI.

## 7. Definition of done
- `make up` funciona sin pasos manuales ocultos.
- `make health` responde `ok`.
- `make audit` queda en verde.
- Secretos fuera de git.
