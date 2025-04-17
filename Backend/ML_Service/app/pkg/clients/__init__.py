from dependency_injector import containers, providers

from .rabbitmq import RabbitMQClient
from .s3 import S3Clients

__all__ = ["Clients", "RabbitMQClient", "S3Clients"]


class Clients(containers.DeclarativeContainer):
    """Containers with clients."""

    s3: S3Clients = providers.Container(S3Clients)
    rabbit_mq = providers.Container(RabbitMQClient)
