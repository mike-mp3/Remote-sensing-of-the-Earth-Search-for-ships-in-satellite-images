"""Container with async redis connector."""

from dependency_injector import containers, providers
from app.pkg.connectors.async_redis.connector import AsyncRedisConnector
from app.pkg.settings import settings

__all__ = ["AsyncRedis"]


class AsyncRedis(containers.DeclarativeContainer):
    """Declarative container with async redis connector."""

    connector = providers.Factory(
        AsyncRedisConnector,
        dsn=settings.REDIS.DSN,
    )