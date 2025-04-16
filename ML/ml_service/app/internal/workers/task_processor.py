import asyncio
from app.pkg.connectors.rabbitmq.connector import RabbitMQConnector
from app.pkg.clients.rabbitmq.producer import RabbitMQProducer
from app.pkg.clients.rabbitmq.consumer import RabbitMQConsumer
from app.pkg.clients.s3.prompter import S3PrompterClient
from app.pkg.clients.s3.model_client import S3ModelClient
from app.internal.services.processor import ImageProcessor
from app.pkg.logger import get_logger

logger = get_logger(__name__)


async def main():
    """Запускает воркер для обработки очереди prompt_processing."""
    try:
        rabbitmq_connector = RabbitMQConnector()

        producer = RabbitMQProducer(rabbitmq_connector)
        consumer = RabbitMQConsumer(rabbitmq_connector)

        s3_prompt_client = S3PrompterClient(
            base_url="http://s3.example.com",
            aws_access_key_id="your_access_key",
            aws_secret_access_key="your_secret_key",
            region_name="your_region"
        )
        s3_model_client = S3ModelClient(
            base_url="http://s3.example.com",
            aws_access_key_id="your_access_key",
            aws_secret_access_key="your_secret_key",
            region_name="your_region"
        )

        processor = ImageProcessor(s3_prompt_client, s3_model_client, producer)

        await consumer.consume_messages(
            queue_name="prompt_processing",
            callback=processor.callback
        )

    except Exception as e:
        logger.error(f"Worker failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
