SHELL := /bin/sh

UV := uv
COMPOSE := docker compose
SERVICE := naas

.DEFAULT_GOAL := help

.PHONY: help install sync lock lock-upgrade \
	lint lint-fix format format-check \
	test test-unit test-functional test-cov check \
	build image-build image-run \
	up down restart ps logs shell clean

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
	$(UV) run ruff check naas tests

lint-fix: ## Fix Ruff errors
	$(UV) run ruff check --fix naas tests

format: ## Format Python files
	$(UV) run ruff format naas tests

format-check: ## Check Python formatting
	$(UV) run ruff format --check naas tests

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
		--cov-report=html

check: format-check lint test-cov ## Run all quality checks

build: ## Build the Docker image
	$(COMPOSE) build

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

image-build: ## Build the application Docker image
	docker build \
		--file $(DOCKERFILE) \
		--tag $(IMAGE):$(IMAGE_TAG) \
		.

image-run: ## Run the application Docker image
	docker run --rm \
		--name $(SERVICE) \
		--publish 5000:5000 \
		$(IMAGE):$(IMAGE_TAG)
