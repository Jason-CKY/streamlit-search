.PHONY: all

start:
	docker-compose up -d

build:
	docker-compose up --build -d

stop:
	docker-compose down

destroy:
	docker-compose down -v

