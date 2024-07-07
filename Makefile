DOCKER := docker
DC := docker compose

.PHONY: start stop up down re
start:
	$(DC) start
stop:
	$(DC) stop
up:
	$(DC) up --build
down:
	$(DC) down
re:
	$(DOCKER) system prune --force
	$(DC) up --build
