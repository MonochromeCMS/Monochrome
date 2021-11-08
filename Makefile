include .env

buildkit ?= 1
test_exit ?= 0
user ?= `id -u`

flavor ?= caddy
project ?= "Monochrome"

DC = DOCKER_BUILDKIT=$(buildkit) docker-compose -p $(project) -f docker-compose.$(flavor).yml

.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: flavors
flavors: ## List all the flavors available
	@echo Flavors available:
	@find . -name 'docker-compose.*.yml' | cut -d "." -f3

.PHONY: build
build:	## Build project with compose
	$(DC) build

.PHONY: build-webui
build-webui:	## Build the webui static files to ./dist
	docker run -v `pwd`:/vol -w /vol --env-file .env.webui node:lts-slim bash ./build-webui.sh

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
logs:	## Read the containers' logs
	$(DC) logs -f --tail 500

.PHONY: logs-%
logs-%: ## Read a container's logs
	$(DC) logs -f --tail 500 $*

.PHONY: sh-%
sh-%: ## Open a shell in a container running container
	$(DC) exec $* sh

.PHONY: secret
secret: ## Generate a secret
	@openssl rand -hex 30

.PHONY: create_admin
create_admin: up-db ## Create a new admin user
	@$(DC) run --rm api create_admin

.PHONY: install
install: build create_admin up ## Create a new instance from scratch
