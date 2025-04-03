"""All redis repositories are defined here."""

from dependency_injector import containers, providers

from app.internal.repository.async_redis.user import UserAsyncRedisRepository


class AsyncRedisRepositories(containers.DeclarativeContainer):
    """Container for postgresql repositories."""

    user_repository = providers.Factory(UserAsyncRedisRepository)