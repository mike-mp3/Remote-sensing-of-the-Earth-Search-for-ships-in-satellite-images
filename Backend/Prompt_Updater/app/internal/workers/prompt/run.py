from time import sleep

from app.internal.services import PromptService, Services
from app.pkg.clients.rabbitmq import RabbitMQClient
from app.pkg.clients.rabbitmq.consumer import RabbitMQConsumer
from app.pkg.logger import get_logger
from app.pkg.settings import settings
from dependency_injector.wiring import Provide, inject

logger = get_logger(__name__)


@inject
async def listen(
    consumer: RabbitMQConsumer = Provide[RabbitMQClient.consumer],
    prompt_service: PromptService = Provide[Services.prompt_service],
):
    await consumer.consume_messages(
        queue_name=settings.RABBIT.RESULT_PROMPTS_QUEUE_NAME,
        callback=prompt_service.callback_handle_results,
    )


async def run():
    while True:
        try:
            await listen()
        except Exception as exc:
            logger.error(exc)
            sleep(10)
