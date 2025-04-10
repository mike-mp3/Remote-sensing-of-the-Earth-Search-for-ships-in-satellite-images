import asyncio
from time import sleep

from app.internal.services import PromptService, Services
from app.pkg.clients.rabbitmq import RabbitMQClient
from app.pkg.clients.rabbitmq.consumer import RabbitMQConsumer
from app.pkg.logger import get_logger
from app.pkg.settings import settings
from dependency_injector.wiring import Provide, inject

logger = get_logger(__name__)


def init_worker(pkg_name):
    """Wire packages during worker initialization to inject dependencies."""
    from app.configuration import __containers__

    __containers__.wire_packages(pkg_name=pkg_name)


def call(body: dict):
    # some logic
    pass


@inject
async def listen(
    consumer: RabbitMQConsumer = Provide[RabbitMQClient.consumer],
    prompt_service: PromptService = Provide[Services.prompt_service],
):
    await consumer.consume_messages(
        queue_name=settings.RABBIT.RAW_PROMPTS_QUEUE_NAME,
        callback=prompt_service.mock_handle_raw,
    )


if __name__ == "__main__":
    init_worker(__name__)
    while True:
        try:
            asyncio.run(listen())
        except Exception as exc:
            logger.error(str(exc))
            sleep(10)
