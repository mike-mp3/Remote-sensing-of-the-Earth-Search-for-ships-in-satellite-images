"""Container with RabbitMQ connector."""

from dependency_injector import containers, providers

from app.pkg.connectors.rabbitmq.connector import RabbitMQConnector
from app.pkg.connectors.rabbitmq.resource import RabbitMQResource
from app.pkg.settings import settings

__all__ = ["RabbitMQ"]


class RabbitMQ(containers.DeclarativeContainer):
    """Declarative container with PostgresSQL connector."""

    connector = providers.Singleton(
        RabbitMQConnector,
        dsn=settings.RABBIT.DSN,
        heartbeat=settings.RABBIT.HEARTBEAT,
    )
    resource = providers.Resource(
        RabbitMQResource,
        connector=connector,
    )