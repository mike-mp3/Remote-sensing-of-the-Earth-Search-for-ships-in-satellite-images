"""Service layer."""

from dependency_injector import containers, providers
from app.internal.repository import Repositories, postgresql
from app.internal.services.city import CityService
from app.internal.services.user import UserService
from app.pkg.clients import Clients

from unittest.mock import Mock

RedisMock = Mock()
RedisMock.create.return_value = "fake result"
redis_mock = RedisMock()


class Services(containers.DeclarativeContainer):
    """Containers with services."""

    repositories: postgresql.Repositories = providers.Container(
        Repositories.postgres,
    )  # type: ignore

    clients: Clients = providers.Container(Clients)

    city_service = providers.Factory(
        CityService,
        city_repository=repositories.city_repository,
    )

    user_service = providers.Factory(
        UserService,
        user_repository=repositories.user_repository,
        email_confirmation=clients.email.user_confirmation,
        redis=redis_mock,
    )

