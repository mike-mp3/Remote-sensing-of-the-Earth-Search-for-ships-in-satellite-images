from app.internal.repository.postgresql import PromptRepository
from app.pkg.clients.s3 import S3PrompterClient
from app.pkg.clients.s3.base_client import BaseS3AsyncClient
from app.pkg.models import (
    PresignedPostRequest,
    ConfirmPromptRequest,
    PromptObjectType,
    ActiveUser,
    CreatePromptCommand,
    Prompt
)
from app.pkg.models.exceptions import (
    InvalidPromptPath,
    RawPromptNowFound,
    RawPromptAlreadyExists
)
from app.pkg.models.exceptions.repository import UniqueViolation


class PromptService:
    s3_prompter_client: S3PrompterClient
    prompt_repository: PromptRepository

    def __init__(
        self,
        s3_prompter_client: BaseS3AsyncClient,
        prompt_repository: PromptRepository,
    ):
        self.s3_prompter_client = s3_prompter_client
        self.prompt_repository = prompt_repository


    async def generate_presigned_post(
        self, request: PresignedPostRequest
    ):
        link = self.s3_prompter_client.generate_new_raw_prompt_link(
            request.user_id
        )
        return await self.s3_prompter_client.create_presigned_post(
            link=link
        )

    async def confirm_prompt(
        self, request: ConfirmPromptRequest, active_user: ActiveUser
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
                )
            )
        except UniqueViolation:
            raise RawPromptAlreadyExists
        return prompt
