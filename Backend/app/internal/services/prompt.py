from app.pkg.clients.s3 import S3PrompterClient
from app.pkg.clients.s3.base_client import BaseS3AsyncClient


class PromptService:
    s3_prompter_client: S3PrompterClient

    def __init__(
        self,
        s3_prompter_client: BaseS3AsyncClient
    ):
        self.s3_prompter_client = s3_prompter_client


    async def get_presigned_post(self):
        res = await self.s3_prompter_client.get_presigned_prompt_url(5252)
        return res
