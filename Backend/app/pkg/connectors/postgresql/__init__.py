"""Container with PostgresSQL connector."""

from app.pkg.connectors.postgresql.resource import Postgresql
from app.pkg.settings import settings
from dependency_injector import containers, providers

__all__ = ["PostgresSQL"]


class PostgresSQL(containers.DeclarativeContainer):
    """Declarative container with PostgresSQL connector."""

    connector = providers.Resource(
        Postgresql,
        dsn=settings.POSTGRES.DSN,
        minsize=settings.POSTGRES.MIN_CONNECTION,
        maxsize=settings.POSTGRES.MAX_CONNECTION,
    )
