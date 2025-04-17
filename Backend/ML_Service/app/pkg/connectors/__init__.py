"""All connectors in declarative container."""

from app.pkg.connectors.rabbitmq import RabbitMQ
from dependency_injector import containers, providers

__all__ = ["Connectors", "RabbitMQ"]


class Connectors(containers.DeclarativeContainer):
    """Declarative container with all connectors."""

    rabbitmq: RabbitMQ = providers.Container(RabbitMQ)
