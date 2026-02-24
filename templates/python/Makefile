SHELL := /bin/bash

COMPOSE_BASE := docker-compose.yml
COMPOSE_DEV := docker-compose.dev.yml
COMPOSE_CI := docker-compose.ci.yml
COMPOSE := docker compose -f $(COMPOSE_BASE) -f $(COMPOSE_DEV)
COMPOSE_TEST := docker compose -f $(COMPOSE_BASE) -f $(COMPOSE_CI)
APP_SERVICE ?= app
HEALTH_URL ?= http://127.0.0.1:8000/health

.PHONY: help bootstrap up down restart logs ps health wait-health sh lint format typecheck test audit ci-test ci-audit clean

help:
	@echo "Targets disponibles:"
	@echo "  make bootstrap  -> crea .env desde .env.example si no existe"
	@echo "  make up         -> levanta stack dev"
	@echo "  make down       -> baja stack y borra volumenes"
	@echo "  make restart    -> reinicia stack"
	@echo "  make logs       -> sigue logs"
	@echo "  make ps         -> estado servicios"
	@echo "  make health     -> comprueba /health"
	@echo "  make wait-health-> espera health con reintentos"
	@echo "  make sh         -> shell en app"
	@echo "  make lint       -> ruff check"
	@echo "  make format     -> ruff format --check"
	@echo "  make typecheck  -> mypy"
	@echo "  make test       -> pytest"
	@echo "  make audit      -> lint + format + typecheck + test"
	@echo "  make ci-test    -> pytest en perfil CI"
	@echo "  make ci-audit   -> audit en perfil CI"
	@echo "  make clean      -> baja y limpia volumenes/imagenes huerfanas"

bootstrap:
	@[ -f .env ] || cp .env.example .env

up: bootstrap
	$(COMPOSE) up --build -d

down:
	$(COMPOSE) down -v --remove-orphans

restart: down up

logs:
	$(COMPOSE) logs -f --tail=200

ps:
	$(COMPOSE) ps

health:
	@curl -fsS "$(HEALTH_URL)" >/dev/null && echo "health: ok" || (echo "health: fail"; exit 1)

wait-health:
	@for i in {1..30}; do \
		curl -fsS "$(HEALTH_URL)" >/dev/null && echo "health: ok" && exit 0; \
		sleep 2; \
	done; \
	echo "health: timeout"; \
	exit 1

sh:
	$(COMPOSE) exec $(APP_SERVICE) sh

lint:
	$(COMPOSE_TEST) run --rm $(APP_SERVICE) ruff check src tests

format:
	$(COMPOSE_TEST) run --rm $(APP_SERVICE) ruff format --check src tests

typecheck:
	$(COMPOSE_TEST) run --rm $(APP_SERVICE) mypy src

test:
	$(COMPOSE_TEST) run --rm $(APP_SERVICE) pytest -q

audit: lint format typecheck test
	@echo "audit: ok"

ci-test:
	$(COMPOSE_TEST) run --rm $(APP_SERVICE) pytest -q

ci-audit:
	$(COMPOSE_TEST) run --rm $(APP_SERVICE) sh -lc "ruff check src tests && ruff format --check src tests && mypy src && pytest -q"

clean:
	$(COMPOSE) down -v --remove-orphans
	docker image prune -f
