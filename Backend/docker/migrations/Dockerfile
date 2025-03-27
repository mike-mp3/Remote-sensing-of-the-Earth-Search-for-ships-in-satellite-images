FROM python:3.13-slim-bookworm

RUN mkdir -p /usr/src/postgres_migrations/
WORKDIR /usr/src/postgres_migrations/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends dos2unix

RUN pip install --upgrade pip

RUN pip install poetry

COPY poetry.lock pyproject.toml /usr/src/postgres_migrations/

RUN poetry install --only main --no-root

COPY . /usr/src/postgres_migrations/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN chmod +x scripts/wait-for-server.sh

RUN dos2unix scripts/*
