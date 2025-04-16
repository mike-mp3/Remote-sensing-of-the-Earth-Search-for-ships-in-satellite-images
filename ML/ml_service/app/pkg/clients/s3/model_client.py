from .base_client import S3AsyncClient
from pydantic import AnyUrl, PositiveInt, SecretStr
from typing import Optional


class S3ModelClient(S3AsyncClient):
    bucket_name = "ml-models"

    def __init__(
        self,
        base_url: AnyUrl,
        aws_access_key_id: str,
        aws_secret_access_key: SecretStr,
        region_name: Optional[str] = None,
    ):
        super().__init__(
            base_url,
            aws_access_key_id,
            aws_secret_access_key,
            region_name,
        )

    async def download_model(self, model_key: str, local_path: str) -> None:
        """Загружает модель из бакета ml-models."""
        model_bytes = await self._download_file(model_key)
        with open(local_path, "wb") as f:
            f.write(model_bytes)
