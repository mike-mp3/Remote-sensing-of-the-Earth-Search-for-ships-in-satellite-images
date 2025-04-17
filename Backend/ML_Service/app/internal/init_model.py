import os

from app.pkg.clients import Clients
from app.pkg.clients.s3 import S3ModelClient
from app.pkg.logger import get_logger
from app.pkg.settings import settings
from dependency_injector.wiring import Provide, inject

logger = get_logger(__name__)


@inject
async def __download_model_if_not_exists(
    s3_model_client: S3ModelClient = Provide[Clients.s3.model],
):
    model_path = settings.ML_MODEL.LOCAL_FULL_PATH
    if not os.path.exists(model_path):
        logger.info("Downloading model to %s", model_path)
        model = await s3_model_client.download()
        with open(model_path, "wb") as file:
            file.write(model)
    else:
        logger.info("Working with existing model: %s", model_path)


@inject
async def __download_model(
    s3_model_client: S3ModelClient = Provide[Clients.s3.model],
):
    model_path = settings.ML_MODEL.LOCAL_FULL_PATH
    logger.info("Downloading model to %s", model_path)

    model = await s3_model_client.download()
    with open(model_path, "wb") as file:
        file.write(model)
