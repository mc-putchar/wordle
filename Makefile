DOCKER := docker
DC := docker compose

up:
	$(DC) up --build
down:
	$(DC) down
start:
	$(DC) start
stop:
	$(DC) stop

re:
	$(DC) --build --force-recreate
