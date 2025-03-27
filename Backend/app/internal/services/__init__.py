"""Service layer."""

from dependency_injector import containers, providers
from app.internal.repository import (
    Repositories,
    postgresql as postgres_module,
    async_redis as async_redis_module
)
from app.internal.services.city import CityService
from app.internal.services.user import UserService
from app.pkg.clients import Clients



class Services(containers.DeclarativeContainer):
    """Containers with services."""

    repositories: postgres_module.Repositories = providers.Container(
        Repositories.postgresql_,
    )  # type: ignore

    async_redis: async_redis_module.AsyncRedisRepositories = providers.Container(
        Repositories.async_redis_
    )

    clients: Clients = providers.Container(Clients)

    city_service = providers.Factory(
        CityService,
        city_repository=repositories.city_repository,
    )

    user_service = providers.Factory(
        UserService,
        user_repository=repositories.user_repository,
        email_confirmation=clients.email.user_confirmation,
        user_redis_repository=async_redis.user_repository,
    )

