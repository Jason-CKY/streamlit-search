.DEFAULT_GOAL := help

# declares .PHONY which will run the make command even if a file of the same name exists
.PHONY: help
help:			## Help command
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: start
start:		## Start docker services
	docker-compose up -d

.PHONY: build
build:		## Build all docker images and start services
	docker-compose up --build -d

.PHONY: stop
stop:		## Stop all docker services
	docker-compose down

.PHONY: destroy
destroy:	## Stop all docker services and deletes all volumes
	docker-compose down -v

