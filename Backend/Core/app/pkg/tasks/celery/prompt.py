from datetime import datetime
from typing import Optional

from app.internal.repository.postgresql import PromptRepository, Repositories
from app.pkg.clients import Clients
from app.pkg.clients.email_client import EmailClient
from app.pkg.clients.s3 import S3PrompterClient
from app.pkg.logger import get_logger
from app.pkg.models import (
    BinaryPrompt,
    DividedBinaryPrompt,
    PromptObjectType,
    PromptStatus,
    ReadPromptWithFilters,
)
from app.pkg.models.exceptions.repository import EmptyResult
from app.pkg.tasks.celery.celery_app import celery_app
from app.pkg.tasks.celery.decorators import async_to_sync
from app.pkg.utils.pdf_generator import generate_pdf
from dependency_injector.wiring import Provide, inject
from pydantic import EmailStr, PositiveInt

logger = get_logger(__name__)


class PromptTasks:
    prompts_repository: PromptRepository
    s3_prompter_client: S3PrompterClient
    email_client: EmailClient

    def __init__(
        self,
        prompts_repository: PromptRepository,
        s3_prompter_client: S3PrompterClient,
        email_client: EmailClient,
    ):
        self.prompts_repository = prompts_repository
        self.s3_prompter_client = s3_prompter_client
        self.email_client = email_client

    # async def __fetch_prompts_data(
    #     self,
    #     user_id: PositiveInt,
    #     start_time: Optional[datetime] = None,
    #     end_time: Optional[datetime] = None,
    #     limit: Optional[PositiveInt] = None,
    # ) -> DividedBinaryPrompt:
    #
    #     raw = []
    #     results = []
    #     prompts = await self.prompts_repository.read_with_filters(
    #         cmd=ReadPromptWithFilters(
    #             user_id=user_id,
    #             status=PromptStatus.success.value,
    #             start_time=start_time,
    #             end_time=end_time,
    #             limit=limit,
    #         ),
    #     )
    #     for prompt in prompts:
    #         raw_link = self.s3_prompter_client.get_prompt_link(
    #             user_id=user_id,
    #             prompt_id=prompt.prompt_id,
    #             prompt_type=PromptObjectType.RAW.value,
    #         )
    #         raw_image = await self.s3_prompter_client.download_image(raw_link)
    #
    #         result_link = self.s3_prompter_client.get_prompt_link(
    #             user_id=user_id,
    #             prompt_id=prompt.prompt_id,
    #             prompt_type=PromptObjectType.RESULT.value,
    #         )
    #         result_image = await self.s3_prompter_client.download_image(result_link)
    #
    #         if raw_image and result_image:
    #             raw.append(BinaryPrompt(**prompt.to_dict(), data=raw_image))
    #             results.append(BinaryPrompt(**prompt.to_dict(), data=result_image))
    #
    #     return DividedBinaryPrompt(raw=raw, results=results)
    #
    #
    # async def generate_and_send_report(
    #     self,
    #     user_id: PositiveInt,
    #     email: EmailStr,
    #     start_time: Optional[datetime] = None,
    #     end_time: Optional[datetime] = None,
    #     limit: Optional[PositiveInt] = None,
    # ):
    #     try:
    #         prompts = await self.__fetch_prompts_data(
    #             user_id=user_id,
    #             start_time=start_time,
    #             end_time=end_time,
    #             limit=limit,
    #         )
    #         report = generate_pdf(prompts.raw, prompts.results)
    #         if not report:
    #             raise ValueError("PDF is empty")
    #
    #         logger.error("Trying to send report to %s", email)
    #         await self.email_client.send_report_about_prompts(
    #             to_email=email,
    #             file=report,
    #         )
    #         logger.error("Report was sent to %s", email)
    #     except EmptyResult:
    #         logger.error(
    #             "Prompts not found for user %s:",
    #             user_id,
    #         )
    #
    #     except Exception as exc:
    #         logger.error(
    #             "Failed to generate report for user %s: %s",
    #             user_id,
    #             exc,
    #         )
    #         raise exc
