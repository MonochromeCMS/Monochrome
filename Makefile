include .env

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

.PHONY: up-%
up-%: ## Start a container
	$(DC) up -d $*

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
	@$(DC) run --rm -w /api api pipenv lock --pre

.PHONY: lint
lint:  ## Lint project code.
	@$(DC) run --rm -w /api api flake8 .
	@$(DC) run --rm -w /api api black . --check --diff

.PHONY: format
format:  ## Format project code.
	@$(DC) run --rm -w /api api black .

.PHONY: upgrade
upgrade: up-db ## Update the database.
	@$(DC) run --rm -T --workdir /api api alembic upgrade head

.PHONY: downgrade
downgrade: up-db ## Downgrade the database.
	@$(DC) run --rm -T --workdir /api api alembic downgrade -1

.PHONY: revision
.ONESHELL: revision
revision rev: up-db ## Create a new database revision.
	@read -p "Revision name: " rev
	@$(DC) run --rm --workdir /api api bash -c "alembic revision --autogenerate -m '$$rev' && chown -R $(user) ./alembic/versions"

.PHONY: secret
secret: ## Generate a secret.
	@openssl rand -base64 31

.PHONY: create_admin
.ONESHELL: create_admin
create_admin: up-db ## Creates a new admin user.
	@read -p "Username: " user
	@read -p "Password: " pass
	@hash=`$(DC) run -T api python -c "from passlib.hash import bcrypt;print(bcrypt.hash('$$pass'), end='')"`
	@id=`$(DC) run -T api python -c "from uuid import uuid4;print(uuid4(), end='')"`
	@$(DC) exec -T db psql $(DB_NAME) $(DB_USER) -c "    \
		INSERT INTO \"user\"                             \
		(version, id, username, hashed_password)         \
		VALUES(                                          \
            1,                                           \
			'$$id',                                      \
			'$$user',                                    \
			'$$hash'                                     \
		);"

.PHONY: install
install: build upgrade up ## Create a new instance from scratch.