"""All redis repositories are defined here."""

from app.internal.repository.async_redis.user import UserAsyncRedisRepository
from dependency_injector import containers, providers


class AsyncRedisRepositories(containers.DeclarativeContainer):
    """Container for postgresql repositories."""

    user_repository = providers.Factory(UserAsyncRedisRepository)
