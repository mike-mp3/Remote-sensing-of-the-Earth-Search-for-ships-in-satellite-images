import io
import os
from typing import Optional

import cv2
import numpy as np
from app.pkg.clients.rabbitmq.producer import RabbitMQProducer
from app.pkg.clients.s3.prompter import S3PrompterClient
from app.pkg.logger import get_logger
from app.pkg.models import RawPromptMessage, ResultPromptMessage
from PIL import Image
from ultralytics import YOLO

logger = get_logger(__name__)


class ImageProcessor:
    s3_prompter_client: S3PrompterClient
    rabbitmq_producer: RabbitMQProducer
    raw_queue_name: str
    results_queue_name: str
    model_file_key: str
    model_local_path: str

    model: Optional[YOLO] = None

    def __init__(
        self,
        s3_prompter_client: S3PrompterClient,
        rabbitmq_producer: RabbitMQProducer,
        raw_queue_name: str,
        results_queue_name: str,
        model_local_path: str,
    ):
        self.s3_prompter_client = s3_prompter_client
        self.rabbitmq_producer = rabbitmq_producer
        self.model_local_path = model_local_path
        self.raw_queue_name = raw_queue_name
        self.results_queue_name = results_queue_name
        # Skip model loading for mock
        self.model = None

    async def callback_handle_raw(self, data: RawPromptMessage):
        # Download raw image from S3
        raw_image = await self.s3_prompter_client.download_image(data.raw_key)

        # Skip ML processing and just use the original image
        result_image = self.__get_result_mock(raw_image)

        # S3 interaction
        link = self.s3_prompter_client.parse_path(data.raw_key)
        result_link = self.s3_prompter_client.get_result_prompt_link(
            user_id=link.user_id,
            prompt_id=link.prompt_id,
        )
        await self.s3_prompter_client.upload_image(
            file_key=result_link.key_path,
            data=result_image,
        )

        # Report the successful completion of processing
        await self.rabbitmq_producer.publish_message(
            message=ResultPromptMessage(
                id=data.id,
                result_key=result_link.key_path,
            ),
            queue_name=self.results_queue_name,
        )

    def __get_result_mock(self, raw_image: bytes) -> bytes:
        """Mock version that just returns the original image without processing"""
        # Just verify it's a valid image and return as is
        image = Image.open(io.BytesIO(raw_image)).convert("RGB")
        
        # Convert back to bytes in the same format as original processing
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()
