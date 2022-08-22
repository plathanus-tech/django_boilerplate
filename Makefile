build:
	docker-compose --env-file .env.dev build

up:
	docker-compose --env-file .env.dev up

down:
	docker-compose --env-file .env.dev down

debug:
	docker-compose f docker-compose.debug.yml --env-file .env.dev up
