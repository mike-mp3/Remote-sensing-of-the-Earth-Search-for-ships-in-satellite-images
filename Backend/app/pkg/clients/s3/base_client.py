from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from typing import Dict, List, Optional, TypeVar

import aioboto3
from app.pkg.logger import get_logger
from botocore.exceptions import ClientError
from pydantic import AnyUrl, SecretStr

logger = get_logger(__name__)

BaseS3AsyncClient = TypeVar("BaseS3AsyncClient", bound="S3AsyncClient")


class S3AsyncClient(ABC):
    def __init__(
        self,
        base_url: AnyUrl,
        aws_access_key_id: str,
        aws_secret_access_key: SecretStr,
        region_name: Optional[str] = None,
    ):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region_name = region_name
        self.base_url = str(base_url)
        self.__session = aioboto3.Session(
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key.get_secret_value(),
            region_name=self.region_name,
        )

    @property
    @abstractmethod
    def bucket_name(self) -> str:
        pass

    @asynccontextmanager
    async def __get_client(self):
        async with self.__session.client(
            service_name="s3",
            endpoint_url=self.base_url,
        ) as client:
            yield client

    async def _upload_file(
        self,
        file_key: str,
        data: bytes,
        content_type: str = "image/",
    ) -> None:
        try:
            async with self.__get_client() as client:
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=file_key,
                    Body=data,
                    ContentType=content_type,
                )
        except ClientError as e:
            logger.error("Error uploading file: %s", e)
            raise e from e

    async def _download_file(self, file_key: str):
        try:
            async with self.__get_client() as client:
                response = await client.get_object(
                    Bucket=self.bucket_name,
                    Key=file_key,
                )
                data = await response["Body"].read()
                return data
        except ClientError as e:
            logger.error("Error downloading file: %s", e)
            raise e from e

    async def _delete_file(self, file_key: str):
        try:
            async with self.__get_client() as client:
                await client.delete_object(
                    Bucket=self.bucket_name,
                    Key=file_key,
                )
        except ClientError as e:
            logger.error("Error deleting file: %s", e)
            raise e from e

    async def _create_presigned_post(
        self,
        file_key: str,
        fields: Optional[Dict[str, str]] = None,
        conditions: Optional[List] = None,
        expires_in: int = 3600,
    ):
        try:
            async with self.__get_client() as client:
                return await client.generate_presigned_post(
                    Bucket=self.bucket_name,
                    Key=file_key,
                    Fields=fields,
                    Conditions=conditions,
                    ExpiresIn=expires_in,
                )
        except ClientError as e:
            logger.error("Error creating presigned post: %s", e)
            raise e from e

    async def _object_exists(self, file_key: str) -> bool:
        try:
            async with self.__get_client() as client:
                await client.head_object(
                    Bucket=self.bucket_name,
                    Key=file_key,
                )
                return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False
            logger.error("Error checking if object %s exists: %s", file_key, e)
            raise e from e
