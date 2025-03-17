"""Service layer."""

from dependency_injector import containers, providers

from app.internal.repository import Repositories, postgresql
from app.internal.services.city import CityService
from app.internal.services.user import UserService


class Services(containers.DeclarativeContainer):
    """Containers with services."""

    repositories: postgresql.Repositories = providers.Container(
        Repositories.postgres,
    )  # type: ignore


    city_service = providers.Factory(
        CityService,
        city_repository=repositories.city_repository,
    )

    user_service = providers.Factory(
        UserService,
        user_repository=repositories.user_repository,
    )

