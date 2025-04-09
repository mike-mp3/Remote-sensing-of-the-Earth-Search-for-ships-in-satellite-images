"""Service layer."""

from app.internal.repository import Repositories
from app.internal.repository import async_redis as async_redis_module
from app.internal.repository import postgresql as postgres_module
from app.internal.services.auth import AuthService
from app.internal.services.prompt import PromptService
from app.internal.services.user import UserService
from app.pkg.clients import Clients
from app.pkg.settings import settings
from dependency_injector import containers, providers


class Services(containers.DeclarativeContainer):
    """Containers with services."""

    repositories: postgres_module.Repositories = providers.Container(
        Repositories.postgresql_,
    )  # type: ignore

    async_redis: async_redis_module.AsyncRedisRepositories = providers.Container(
        Repositories.async_redis_,
    )

    clients: Clients = providers.Container(Clients)

    user_service = providers.Factory(
        UserService,
        user_repository=repositories.user_repository,
        email_confirmation=clients.email.user_confirmation,
        user_redis_repository=async_redis.user_repository,
    )

    auth_service = providers.Factory(
        AuthService,
        refresh_token_repository=repositories.refresh_token_repository,
        user_repository=repositories.user_repository,
    )

    prompt_service = providers.Factory(
        PromptService,
        s3_prompter_client=clients.s3.prompter,
        prompt_repository=repositories.prompt_repository,
        producer=clients.rabbit_mq.producer,
        raw_queue_name=settings.RABBIT.RAW_PROMPTS_QUEUE_NAME,
    )
