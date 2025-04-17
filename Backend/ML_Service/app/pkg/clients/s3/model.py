from typing import Optional

from pydantic import AnyUrl, SecretStr

from .base_client import S3AsyncClient


class S3ModelClient(S3AsyncClient):
    bucket_name = "ml-models"

    def __init__(
        self,
        base_url: AnyUrl,
        aws_access_key_id: str,
        aws_secret_access_key: SecretStr,
        key_path: str,
        region_name: Optional[str] = None,
    ):
        super().__init__(
            base_url,
            aws_access_key_id,
            aws_secret_access_key,
            region_name,
        )
        self.key_path = key_path

    async def download(self) -> bytes:
        return await self._download_file(self.key_path)
