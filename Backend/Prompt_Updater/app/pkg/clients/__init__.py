from dependency_injector import containers, providers

from .rabbitmq import RabbitMQClient
from .websocket import WebSocket

__all__ = ["Clients"]


class Clients(containers.DeclarativeContainer):
    """Containers with clients."""

    websocket: WebSocket = providers.Container(WebSocket)
    rabbit_mq = providers.Container(RabbitMQClient)
