"""Service layer."""

from app.internal.repository import Repositories
from app.internal.repository import postgresql as postgres_module
from app.internal.services.prompt import PromptService
from app.pkg.clients import Clients
from app.pkg.settings import settings
from dependency_injector import containers, providers


class Services(containers.DeclarativeContainer):
    """Containers with services."""

    repositories: postgres_module.Repositories = providers.Container(
        Repositories.postgresql_,
    )  # type: ignore

    clients: Clients = providers.Container(Clients)

    prompt_service = providers.Factory(
        PromptService,
        prompt_repository=repositories.prompt_repository,
        producer=clients.rabbit_mq.producer,
        websocket_manager=clients.websocket.manager,
        raw_queue_name=settings.RABBIT.RAW_PROMPTS_QUEUE_NAME,
    )
