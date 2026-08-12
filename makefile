SHELL := /bin/sh

UV := uv
COMPOSE := docker compose
SERVICE := naas

PYTHON_DIRS := naas tests scripts
DOCKERFILE := naas.Dockerfile
IMAGE_NAME ?= no-as-a-service
IMAGE_TAG ?= latest

.DEFAULT_GOAL := help

.PHONY: help install sync lock lock-upgrade \
	lint lint-fix format format-check \
	test test-unit test-functional test-cov check \
	security-python security pre-commit pre-commit-run \
	build up down restart ps logs shell clean image-build image-run image-push

help: ## Display available commands
	@echo "Available commands:"
	@awk 'BEGIN {FS = ":.*## "}; /^[a-zA-Z0-9_-]+:.*## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install and synchronize all dependencies
	$(UV) sync

sync: ## Synchronize the environment from uv.lock
	$(UV) sync --locked

lock: ## Create or update the lock file
	$(UV) lock

lock-upgrade: ## Upgrade all dependencies and update uv.lock
	$(UV) lock --upgrade

lint: ## Run Ruff checks
	$(UV) run ruff check $(PYTHON_DIRS)

lint-fix: ## Fix Ruff errors
	$(UV) run ruff check --fix $(PYTHON_DIRS)

format: ## Format Python files
	$(UV) run ruff format $(PYTHON_DIRS)

format-check: ## Check Python formatting
	$(UV) run ruff format --check $(PYTHON_DIRS)

test: ## Run all tests
	$(UV) run pytest

test-unit: ## Run unit tests
	$(UV) run pytest -m unit tests/unit

test-functional: ## Run functional tests
	$(UV) run pytest -m functional tests/functional

test-cov: ## Run tests with coverage
	$(UV) run pytest \
		--cov=naas \
		--cov-branch \
		--cov-report=term-missing \
		--cov-report=html \
		--cov-fail-under=80

security-python: ## Python security checks
	$(UV) run bandit -r naas scripts -ll
	$(UV) run pip-audit --skip-editable

security: ## All local security checks
	$(UV) run pre-commit run --all-files

check: format-check lint test-cov security-python ## Run all quality + security checks

pre-commit: ## Install local pre-commit and pre-push hooks
	$(UV) run pre-commit install
	$(UV) run pre-commit install --hook-type pre-push

pre-commit-run: ## Run all pre-commit hooks
	$(UV) run pre-commit run --all-files

build: ## Build the Docker image
	$(COMPOSE) build

image-build: ## Build application docker image with the project dockerfile
	docker build -f $(DOCKERFILE) -t $(IMAGE_NAME):$(IMAGE_TAG) .

image-run: ## Run image locally
	docker run --rm -p 5000:5000 --name $(SERVICE) $(IMAGE_NAME):$(IMAGE_TAG)

image-push: ## Push local image
	docker push $(IMAGE_NAME):$(IMAGE_TAG)

up: ## Start all services
	$(COMPOSE) up -d --build

down: ## Stop and remove services
	$(COMPOSE) down --remove-orphans

restart: ## Restart all services
	$(COMPOSE) restart

ps: ## Show service status
	$(COMPOSE) ps

logs: ## Follow logs
	$(COMPOSE) logs -f --tail=100

shell: ## Open a shell in the application container
	$(COMPOSE) exec $(SERVICE) /bin/sh

clean: ## Remove generated files
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf .coverage
	rm -rf htmlcov
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
