from app.pkg.clients.websocket.manager import WebSocketManager
from dependency_injector import containers, providers

__all__ = ["WebSocket"]


class WebSocket(containers.DeclarativeContainer):
    """WebSocket container."""

    manager = providers.Singleton(WebSocketManager)
