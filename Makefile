SHELL := /bin/bash

poetry:
	docker-compose exec app poetry add $(package)

build:
	docker-compose build

black:
	docker-compose exec app black .

flake:
	docker-compose exec app flake8 .

stop:
	docker-compose stop
