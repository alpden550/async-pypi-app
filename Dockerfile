FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VIRTUALENVS_CREATE=false
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add gcc python3-dev musl-dev build-base postgresql-dev libffi-dev\
    && apk add zlib-dev cairo-dev pango-dev gdk-pixbuf-dev \
    && apk add openssl-dev cargo


RUN pip install --upgrade pip
RUN pip install poetry

COPY pyproject.toml /app/pyproject.toml
COPY poetry.lock /app/poetry.lock

RUN poetry install

COPY . /app

EXPOSE 8000
EXPOSE 443

ENTRYPOINT ["/app/entrypoint.sh"]
