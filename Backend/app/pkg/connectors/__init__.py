"""All connectors in declarative container."""

from dependency_injector import containers, providers

from app.pkg.connectors.postgresql import PostgresSQL

__all__ = ["Connectors", "PostgresSQL", "AsyncRedis"]

from app.pkg.connectors.async_redis import AsyncRedis


class Connectors(containers.DeclarativeContainer):
    """Declarative container with all connectors."""

    postgresql: PostgresSQL = providers.Container(PostgresSQL)
    async_redis: AsyncRedis = providers.Container(AsyncRedis)

