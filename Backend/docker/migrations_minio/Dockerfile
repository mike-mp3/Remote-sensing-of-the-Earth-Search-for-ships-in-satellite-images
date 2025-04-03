FROM python:3.13-slim-bookworm

RUN mkdir -p /usr/src/minio_migrations/
WORKDIR /usr/src/minio_migrations/

RUN apt-get update &&  \
    apt-get install -y --no-install-recommends dos2unix curl

RUN curl -fsSL https://dl.min.io/client/mc/release/linux-amd64/mc -o /usr/local/bin/mc && \
    chmod +x /usr/local/bin/mc

COPY /migrations_minio/ ./migrations_minio/
COPY /scripts/ ./scripts/

RUN chmod +x scripts/wait-for-server.sh

RUN dos2unix scripts/*
