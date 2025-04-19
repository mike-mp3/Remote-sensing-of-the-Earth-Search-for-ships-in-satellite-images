from typing import Optional, Type
from uuid import uuid4

from app.pkg.models import GeneratePrompt, PromptLink, PromptObjectType
from pydantic import AnyUrl, PositiveInt, SecretStr

from .base_client import S3AsyncClient
from .path_strategies.base import BasePathStrategy
from .path_strategies.prompter import PrompterPathStrategy


class S3PrompterClient(S3AsyncClient):
    bucket_name = "user-prompts"
    _path_strategy: Type[PrompterPathStrategy]

    def __init__(
        self,
        base_url: AnyUrl,
        aws_access_key_id: str,
        aws_secret_access_key: SecretStr,
        path_strategy: Type[BasePathStrategy],
        region_name: Optional[str] = None,
    ):
        super().__init__(
            base_url,
            aws_access_key_id,
            aws_secret_access_key,
            region_name,
        )
        self._path_strategy = path_strategy

    def generate_new_raw_prompt_link(self, user_id: PositiveInt) -> PromptLink:
        prompt_id = uuid4().hex[:10]
        return self._path_strategy.generate_path(
            cmd=GeneratePrompt(
                object_type=PromptObjectType.RAW.value,
                user_id=user_id,
                prompt_id=prompt_id,
            ),
        )

    def get_prompt_link(
        self,
        user_id: str,
        prompt_id: str,
        prompt_type: PromptObjectType,
    ) -> PromptLink:
        return self._path_strategy.generate_path(
            cmd=GeneratePrompt(
                object_type=prompt_type,
                user_id=user_id,
                prompt_id=prompt_id,
            ),
        )

    def parse_path(self, path: str) -> Optional[PromptLink]:
        return self._path_strategy.parse(path)

    async def create_presigned_post(self, link: PromptLink):
        fields_ = {
            "Content-Type": "image/",
        }
        conditions = [
            ["content-length-range", 1024, 10 * 1024 * 1024],  # 10 MB
            ["starts-with", "$Content-Type", "image/"],
        ]
        presigned_data = await self._create_presigned_post(
            file_key=link.key_path,
            fields=fields_,
            conditions=conditions,
            expires_in=600,
        )
        return presigned_data

    async def create_presigned_get(self, link: PromptLink):
        return await self._create_presigned_get(
            file_key=link.key_path,
            expires_in=1200,
        )

    async def object_exists(self, link: PromptLink) -> bool:
        return await self._object_exists(link.key_path)
