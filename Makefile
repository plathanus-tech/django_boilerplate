build:
	- sudo rm -r docker
	docker-compose build

up:
	docker-compose up

debug:
	docker-compose f docker-compose.debug.yml --env-file .env.dev up
