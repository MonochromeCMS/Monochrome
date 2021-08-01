compose_file ?= "docker-compose.yml"
project ?= "Monochrome"

DC = docker-compose -p $(project) -f $(compose_file)

.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: build
build:	## Build project with compose
	$(DC) build

.PHONY: up
start up:	## Run project with compose
	$(DC) up --remove-orphans -d

.PHONY: down
down: ## Reset project containers with compose
	$(DC) down

.PHONY: lock
lock:	## Refresh pipfile.lock
	pipenv lock --pre

.PHONY: lint
lint:  ## Lint project code.
	$(DC) run --rm -w /api api flake8 .
	$(DC) run --rm -w /api api black . --check --diff

.PHONY: format
format:  ## Format project code.
	$(DC) run --rm -w /api api black .

.PHONY: upgrade
upgrade: start ## Update the database.
	$(DC) exec -T --workdir /api api alembic upgrade head

.PHONY: downgrade
downgrade: start ## Downgrade the database.
	$(DC) exec -T --workdir /api api alembic downgrade -1

.PHONY: revision
revision rev: start ## Create a new database revision.
	@read -p "Revision name: " rev; \
	$(DC) exec --workdir /api api alembic revision --autogenerate -m "$$rev"