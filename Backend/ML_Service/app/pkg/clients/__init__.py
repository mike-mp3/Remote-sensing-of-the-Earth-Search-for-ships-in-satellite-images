from dependency_injector import containers, providers

from .email_client.template import Templates
from .rabbitmq import RabbitMQClient
from .s3 import S3Clients

__all__ = ["Clients"]


class Clients(containers.DeclarativeContainer):
    """Containers with clients."""

    email: Templates = providers.Container(Templates)
    s3: S3Clients = providers.Container(S3Clients)
    rabbit_mq = providers.Container(RabbitMQClient)
