.PHONY: help install test run compose-up compose-down compose-logs clean

APP_NAME = nlp-pipeline-service
PORT ?= 8000

help:
	@echo "nlp-pipeline-service Commands:"
	@echo "  make install       - Create .venv and install dependencies"
	@echo "  make test          - Run pytest suite"
	@echo "  make run           - Run FastAPI locally with live reload (port $(PORT))"
	@echo "  make compose-up    - Start container via docker compose (port $(PORT))"
	@echo "  make compose-down  - Stop all running containers & free ports"
	@echo "  make compose-logs  - Stream container output logs"
	@echo "  make clean         - Clean bytecode and pytest cache"

install:
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt
	@if [ ! -f .env ]; then cp .env.example .env; echo "Created .env from .env.example"; fi

test:
	.venv/bin/pytest -v

run:
	.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port $(PORT) --reload

compose-up:
	PORT=$(PORT) docker compose up -d --build

compose-down:
	docker compose down --remove-orphans
	@docker rm -f nlp-service $(APP_NAME) 2>/dev/null || true

compose-logs:
	docker compose logs -f

clean:
	rm -rf __pycache__ .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +