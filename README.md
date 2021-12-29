# Async Pypi App

Clone of PyPi using FastAPI, async SQLAlchemy, Chameleon, Postgres and Traefik.

Demo: https://pypi.shorten.ru.com

## How to prepare

Fill `.env` from `.env.example`

## How to start

Start docker-compose service

```shell
docker-compose up
```

And add sample pypi data

```shell
docker-compose exec app python pypi/bin/load_packages.py
```
