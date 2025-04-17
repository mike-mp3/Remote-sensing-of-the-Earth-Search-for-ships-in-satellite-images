FROM python:3.13-slim-bookworm

RUN mkdir -p /usr/src/worker/
WORKDIR /usr/src/worker/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN pip install poetry

COPY poetry.lock pyproject.toml /usr/src/worker/

RUN poetry install --only main --no-root

COPY . /usr/src/worker/

RUN poetry install --only-root
