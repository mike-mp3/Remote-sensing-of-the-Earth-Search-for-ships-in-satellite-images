"""Container with RabbitMQ connector."""

from dependency_injector import containers, providers

from app.pkg.connectors.rabbitmq.connector import RabbitMQConnector
from app.pkg.connectors import RabbitMQ
from .producer import RabbitMQProducer

__all__ = ['RabbitMQClient']


class RabbitMQClient(containers.DeclarativeContainer):
    """Declarative container with PostgresSQL connector."""

    connection = providers.Container(RabbitMQ)

    producer = providers.Singleton(
        RabbitMQProducer,
        connector=connection.connector,
    )