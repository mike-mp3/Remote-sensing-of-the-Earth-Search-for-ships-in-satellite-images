from aio_pika.exceptions import AMQPConnectionError, ChannelClosed
from app.internal.repository.postgresql import PromptRepository
from app.internal.repository.repository import BaseRepository
from app.pkg.clients.rabbitmq.producer import RabbitMQProducer
from app.pkg.clients.s3 import S3PrompterClient
from app.pkg.clients.s3.base_client import BaseS3AsyncClient
from app.pkg.logger import get_logger
from app.pkg.models import (
    ActiveUser,
    ConfirmPromptRequest,
    CreatePromptCommand,
    PresidnedGetResponse,
    PresignedGetRequest,
    PresignedPostRequest,
    Prompt,
    PromptObjectType,
    PromptPageRequest,
    PromptStatus,
    RawPromptMessage,
    ReadPromptCommand,
    ReadPromptPageCommand,
    SendPromptReportRequest,
)
from app.pkg.models.exceptions import (
    CannotProcessPrompt,
    InvalidPromptPath,
    PromptNotFound,
    RawPromptAlreadyExists,
    RawPromptNowFound,
    UnknownPromptStatus,
)
from app.pkg.models.exceptions.repository import EmptyResult, UniqueViolation
from app.pkg.tasks.celery.prompt import PromptTasks

logger = get_logger(__name__)


class PromptService:
    s3_prompter_client: S3PrompterClient
    prompt_repository: PromptRepository
    producer: RabbitMQProducer
    raw_queue_name: str
    prompt_tasks: PromptTasks

    def __init__(
        self,
        s3_prompter_client: BaseS3AsyncClient,
        prompt_repository: BaseRepository,
        producer: RabbitMQProducer,
        raw_queue_name: str,
        prompt_tasks: PromptTasks,
    ):
        self.s3_prompter_client = s3_prompter_client
        self.prompt_repository = prompt_repository
        self.producer = producer
        self.raw_queue_name = raw_queue_name
        self.prompt_tasks = prompt_tasks

    async def generate_presigned_post(
        self,
        request: PresignedPostRequest,
    ):
        link = self.s3_prompter_client.generate_new_raw_prompt_link(
            request.user_id,
        )
        return await self.s3_prompter_client.create_presigned_post(
            link=link,
        )

    async def confirm_prompt(
        self,
        request: ConfirmPromptRequest,
        active_user: ActiveUser,
    ) -> Prompt:
        link = self.s3_prompter_client.parse_path(request.key_path)
        if not link:
            raise InvalidPromptPath
        if link.object_type != PromptObjectType.RAW.value or link.user_id != active_user.id:
            raise InvalidPromptPath

        if not await self.s3_prompter_client.object_exists(link):
            raise RawPromptNowFound

        try:
            prompt = await self.prompt_repository.create(
                cmd=CreatePromptCommand(
                    user_id=link.user_id,
                    prompt_id=link.prompt_id,
                    raw_key=link.key_path,
                ),
            )
            await self.producer.publish_message(
                RawPromptMessage(**prompt.to_dict()),
                self.raw_queue_name,
            )
        except UniqueViolation:
            raise RawPromptAlreadyExists
        except (AMQPConnectionError, ChannelClosed):
            raise CannotProcessPrompt

        return prompt

    async def get_page(
        self,
        request: PromptPageRequest,
        active_user: ActiveUser,
    ):
        try:
            if request.created_at and request.prompt_id:
                prompts = await self.prompt_repository.read_page(
                    cmd=ReadPromptPageCommand(
                        user_id=active_user.id,
                        size=request.size,
                        prompt_id=request.prompt_id,
                        created_at=request.created_at,
                    ),
                )
            else:
                prompts = await self.prompt_repository.read(
                    cmd=ReadPromptCommand(
                        user_id=active_user.id,
                        size=request.size,
                    ),
                )
            return prompts
        except EmptyResult:
            raise PromptNotFound

    async def generate_presigned_get(
        self,
        request: PresignedGetRequest,
        active_user: ActiveUser,
    ):
        prompts = []
        for prompt in request.prompts:
            if prompt.status in (PromptStatus.pending.value, PromptStatus.success.value):
                link = self.s3_prompter_client.get_prompt_link(
                    user_id=active_user.id,
                    prompt_id=prompt.prompt_id,
                    prompt_type=PromptObjectType.RAW.value,
                )
            elif prompt.status == PromptStatus.success.value:
                link = self.s3_prompter_client.get_prompt_link(
                    user_id=active_user.id,
                    prompt_id=prompt.prompt_id,
                    prompt_type=PromptObjectType.RESULT.value,
                )
            else:
                raise UnknownPromptStatus

            url = await self.s3_prompter_client.create_presigned_get(
                link=link,
            )
            prompts.append(
                PresidnedGetResponse(
                    prompt_id=prompt.prompt_id,
                    url=url,
                ),
            )
        return prompts

    async def generate_and_send_report(
        self,
        request: SendPromptReportRequest,
        active_user: ActiveUser,
    ):
        self.prompt_tasks.generate_and_send_report.delay(
            user_id=active_user.id,
            email=active_user.email,
            start_time=request.start_time,
            end_time=request.end_time,
            limit=request.limit,
        )
