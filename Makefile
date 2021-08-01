user ?= `id -u`

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

.PHONY: logs
logs:	## Read the containers' logs.
	$(DC) logs -f

.PHONY: logs-%
logs-%: ## Read a container's logs.
	$(DC) logs -f $*

.PHONY: sh-%
sh-%: ## Open a shell in a container running container.
	$(DC) exec $* sh

.PHONY: lock
lock:	## Refresh pipfile.lock
	$(DC) run --rm -w /api api pipenv lock --pre

.PHONY: lint
lint:  ## Lint project code.
	$(DC) run --rm -w /api api flake8 .
	$(DC) run --rm -w /api api black . --check --diff

.PHONY: format
format:  ## Format project code.
	$(DC) run --rm -w /api api black .

.PHONY: upgrade
upgrade: ## Update the database.
	$(DC) run --rm -T --workdir /api api alembic upgrade head

.PHONY: downgrade
downgrade: ## Downgrade the database.
	$(DC) run --rm -T --workdir /api api alembic downgrade -1

.PHONY: revision
revision rev: ## Create a new database revision.
	@read -p "Revision name: " rev; \
	$(DC) run --rm --workdir /api api bash -c "alembic revision --autogenerate -m '$$rev' && chown -R $(user) ./alembic/versions"
