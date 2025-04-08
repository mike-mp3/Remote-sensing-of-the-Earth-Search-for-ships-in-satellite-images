"""All connectors in declarative container."""

from dependency_injector import containers, providers

from app.pkg.connectors.postgresql import PostgresSQL
from app.pkg.connectors.async_redis import AsyncRedis
from app.pkg.connectors.rabbitmq import RabbitMQ

__all__ = ["Connectors", "PostgresSQL", "AsyncRedis", "RabbitMQ"]


class Connectors(containers.DeclarativeContainer):
    """Declarative container with all connectors."""

    postgresql: PostgresSQL = providers.Container(PostgresSQL)
    async_redis: AsyncRedis = providers.Container(AsyncRedis)
    rabbitmq: RabbitMQ = providers.Container(RabbitMQ)

