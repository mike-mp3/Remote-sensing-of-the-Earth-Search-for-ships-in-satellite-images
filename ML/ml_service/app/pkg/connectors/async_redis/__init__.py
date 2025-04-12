"""Container with async redis connector."""

from app.pkg.connectors.async_redis.connector import AsyncRedisConnector
from app.pkg.settings import settings
from dependency_injector import containers, providers

__all__ = ["AsyncRedis"]


class AsyncRedis(containers.DeclarativeContainer):
    """Declarative container with async redis connector."""

    connector = providers.Factory(
        AsyncRedisConnector,
        dsn=settings.REDIS.DSN,
    )
