"""All postgresql repositories are defined here."""

from dependency_injector import containers, providers

from app.internal.repository.postgresql.city import CityRepository


class Repositories(containers.DeclarativeContainer):
    """Container for postgresql repositories."""

    city_repository = providers.Factory(CityRepository)
