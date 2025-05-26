import asyncio
from time import sleep

from app.internal import __containers__
from app.internal.init_model import __download_model, __download_model_if_not_exists
from app.internal.services import ImageProcessor, Services
from app.pkg.clients.rabbitmq import RabbitMQClient
from app.pkg.clients.rabbitmq.consumer import RabbitMQConsumer
from app.pkg.logger import get_logger
from app.pkg.settings import settings
from dependency_injector.wiring import Provide, inject

logger = get_logger(__name__)


def __init_worker(pkg_name):
    __containers__.wire_packages(pkg_name)


@inject
async def listen(
    consumer: RabbitMQConsumer = Provide[RabbitMQClient.consumer],
    image_processor: ImageProcessor = Provide[Services.image_processor],
):
    await consumer.consume_messages(
        queue_name=settings.RABBIT.RAW_PROMPTS_QUEUE_NAME,
        callback=image_processor.callback_handle_raw,
    )


async def main():
    if settings.ML_MODEL.DOWNLOAD:
        await __download_model()
    else:
        await __download_model_if_not_exists()
    while True:
        try:
            await listen()
        except Exception as exc:
            logger.error(exc)
            sleep(10)


if __name__ == "__main__":
    __init_worker(__name__)
    asyncio.run(main())
