"""Container with RabbitMQ connector."""

from app.pkg.connectors import RabbitMQ
from dependency_injector import containers, providers

from .consumer import RabbitMQConsumer
from .producer import RabbitMQProducer

__all__ = ["RabbitMQClient", "RabbitMQ"]


class RabbitMQClient(containers.DeclarativeContainer):
    """Declarative container with PostgresSQL connector."""

    connection = providers.Container(RabbitMQ)

    producer = providers.Singleton(
        RabbitMQProducer,
        connector=connection.connector,
    )

    consumer = providers.Singleton(
        RabbitMQConsumer,
        connector=connection.connector,
    )
