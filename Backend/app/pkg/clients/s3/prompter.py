from typing import Optional, Type
from uuid import uuid4
from pydantic import PositiveInt, AnyUrl, SecretStr

from app.pkg.models import PromptLink, GeneratePromptLink, PrompterClientResponse, PromptObjectType
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
        prompt_id = uuid4().hex[:6]
        return self._path_strategy.generate_path(
            cmd=GeneratePromptLink(
                object_type=PromptObjectType.RAW.value,
                user_id=user_id,
                prompt_id=prompt_id
            )
        )

    async def get_presigned_prompt_url(
        self,
        user_id: PositiveInt
    ) -> PrompterClientResponse:

        link = self.generate_new_raw_prompt_link(user_id)
        fields_ = {
            "Content-Type": "image/"
        }
        conditions = [
            ["content-length-range", 1024, 10 * 1024 * 1024], # 10 MB
            ["starts-with", "$key", link.key_starts_with],
            ["starts-with", "$Content-Type", "image/"],
        ]
        presigned_data = await self._create_presigned_post(
            file_key=link.key_path,
            fields=fields_,
            conditions=conditions,
            expires_in=600
        )

        return PrompterClientResponse(
            s3_response=presigned_data,
            link=link,
        )
