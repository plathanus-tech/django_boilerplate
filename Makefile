build:
	docker-compose build

up:
	docker-compose --env-file .env.dev up

debug:
	docker-compose f docker-compose.debug.yml --env-file .env.dev up
