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

    def get_result_prompt_link(
        self,
        user_id: str,
        prompt_id: str,
    ) -> PromptLink:

        return self._path_strategy.generate_path(
            cmd=GeneratePrompt(
                object_type=PromptObjectType.RESULT.value,
                user_id=user_id,
                prompt_id=prompt_id,
            ),
        )

    def parse_path(self, path: str) -> Optional[PromptLink]:
        return self._path_strategy.parse(path)

    async def upload_image(self, file_key: str, data):
        return await self._upload_file(file_key, data)

    async def download_image(self, file_key: str) -> bytes:
        return await self._download_file(file_key)
