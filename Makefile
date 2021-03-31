build:
	docker-compose build mindfiner
run:
	docker-compose up mindfiner

makemigrations:
	docker-compose up makemigrations

migrate:
	docker-compose up migrate