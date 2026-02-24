SHELL := /bin/bash

COMPOSE ?= docker compose -f docker-compose.yml -f docker-compose.dev.yml
APP_SERVICE ?= app
HEALTH_URL ?= http://127.0.0.1:8000/health

.PHONY: help up down logs ps health lint format typecheck test audit

help:
	@echo "Targets:"
	@echo "  make up        -> Levanta stack local"
	@echo "  make down      -> Baja stack y borra volumenes"
	@echo "  make logs      -> Sigue logs del compose"
	@echo "  make ps        -> Lista servicios"
	@echo "  make health    -> Verifica endpoint /health"
	@echo "  make lint      -> Ruff check"
	@echo "  make format    -> Ruff format --check"
	@echo "  make typecheck -> Mypy"
	@echo "  make test      -> Pytest"
	@echo "  make audit     -> Lint + Typecheck + Test"

up:
	$(COMPOSE) up --build -d

down:
	$(COMPOSE) down -v

logs:
	$(COMPOSE) logs -f --tail=200

ps:
	$(COMPOSE) ps

health:
	@curl -fsS "$(HEALTH_URL)" >/dev/null && echo "health: ok" || (echo "health: fail"; exit 1)

lint:
	$(COMPOSE) run --rm $(APP_SERVICE) ruff check src tests

format:
	$(COMPOSE) run --rm $(APP_SERVICE) ruff format --check src tests

typecheck:
	$(COMPOSE) run --rm $(APP_SERVICE) mypy src

test:
	$(COMPOSE) run --rm $(APP_SERVICE) pytest -q

audit: lint format typecheck test
	@echo "audit: ok"
