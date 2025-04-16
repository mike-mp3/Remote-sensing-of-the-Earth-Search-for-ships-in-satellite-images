import io
import json
import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO
from app.pkg.clients.s3.prompter import S3PrompterClient
from app.pkg.clients.s3.model_client import S3ModelClient
from app.pkg.clients.rabbitmq.producer import RabbitMQProducer
from app.configuration.logger.logger import get_logger
from app.pkg.models import RawPromptMessage, ResultPromptMessage

logger = get_logger(__name__)


class ImageProcessor:
    def __init__(
        self,
        s3_prompt_client: S3PrompterClient,
        s3_model_client: S3ModelClient,
        rabbitmq_producer: RabbitMQProducer
    ):
        self.s3_prompt_client = s3_prompt_client
        self.s3_model_client = s3_model_client
        self.rabbitmq_producer = rabbitmq_producer
        self.model = self._load_model_from_s3()
        logger.info("YOLOv11 model loaded successfully from S3")

    def _load_model_from_s3(self):
        """
        Загружает модель YOLOv11 из S3.
        """
        model_key = "models/yolov11x.pt"
        local_model_path = "/tmp/yolov11x.pt"
        self.s3_model_client.download_model(model_key, local_model_path)
        return YOLO(local_model_path)

    async def callback(self, ch, method, properties, body):
        """
        Callback-функция для обработки сообщений из очереди.
        """
        try:
            # Валидируем входящее сообщение с помощью RawPromptMessage
            task_data = RawPromptMessage(**json.loads(body.decode()))
            logger.info(f"Received task: {task_data.dict()}")

            # Загружаем изображение из S3
            image_bytes = await self.s3_prompt_client.download_image(task_data.raw_key)
            image_np = np.array(Image.open(io.BytesIO(image_bytes)))
            logger.info(f"Image downloaded from S3, key: {task_data.raw_key}")

            # Обрабатываем изображение с помощью YOLOv11
            results = self.model.predict(image_np)
            result_image = results[0].plot(show=False)
            result_image_rgb = cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB)

            # Кодирование в PNG
            success, encoded_image = cv2.imencode(".png", result_image_rgb)
            if not success:
                logger.error("Failed to encode image to PNG")
                raise Exception("Image encoding failed")

            # Создание буфера
            buffer = io.BytesIO(encoded_image.tobytes())
            buffer.seek(0)

            # Сохраняем результат в S3
            result_key = f"user-prompts/results/user_{task_data.user_id}/prompt_{task_data.prompt_id}/result.png"
            await self.s3_client.upload_result(result_key, buffer.getvalue())
            logger.info(f"Result uploaded to S3, key: {result_key}")

            # Формируем исходящее сообщение с помощью ResultPromptMessage
            result_message = ResultPromptMessage(
                id=task_data.id,
                result_key=result_key
            )
            await self.rabbitmq_producer.publish_message(
                message=result_message,
                queue_name="prompt_result"
            )
            logger.info(f"Result published to prompt_result queue: {result_message.dict()}")

        except Exception as e:
            logger.error(f"Error processing task: {e}")
            # Отправляем сообщение об ошибке
            error_message = ResultPromptMessage(
                id=task_data.id if 'task_data' in locals() else None,
                result_key=""
            )
            await self.rabbitmq_producer.publish_message(
                error_message,
                "prompt_result"
            )
