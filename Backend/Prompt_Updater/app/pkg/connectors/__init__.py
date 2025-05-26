"""All connectors in declarative container."""

from app.pkg.connectors.postgresql import PostgresSQL
from app.pkg.connectors.rabbitmq import RabbitMQ
from dependency_injector import containers, providers

__all__ = ["Connectors", "PostgresSQL", "RabbitMQ"]


class Connectors(containers.DeclarativeContainer):
    """Declarative container with all connectors."""

    postgresql: PostgresSQL = providers.Container(PostgresSQL)
    rabbitmq: RabbitMQ = providers.Container(RabbitMQ)
