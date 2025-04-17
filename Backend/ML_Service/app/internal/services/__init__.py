"""Service layer."""
from app.pkg.clients import Clients
from app.pkg.settings import settings
from dependency_injector import containers, providers

from .image_processor import ImageProcessor


class Services(containers.DeclarativeContainer):
    """Containers with services."""

    clients: Clients = providers.Container(Clients)

    image_processor = providers.Factory(
        ImageProcessor,
        s3_prompter_client=clients.s3.prompter,
        rabbitmq_producer=clients.rabbit_mq.producer,
        raw_queue_name=settings.RABBIT.RAW_PROMPTS_QUEUE_NAME,
        model_local_path=settings.ML_MODEL.LOCAL_FULL_PATH,
        results_queue_name=settings.RABBIT.RESULT_PROMPTS_QUEUE_NAME,
    )
