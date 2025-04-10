import aio_pika
from aio_pika.exceptions import AMQPConnectionError, ChannelClosed
from app.pkg.connectors.rabbitmq.connector import RabbitMQConnector
from app.pkg.logger import get_logger
from app.pkg.models.base import BaseModel

__all__ = ["RabbitMQProducer"]

logger = get_logger(__name__)


class RabbitMQProducer:
    def __init__(self, connector: RabbitMQConnector):
        self.conn = connector

    async def publish_message(self, message: BaseModel, queue_name: str):
        try:
            async with self.conn.get_channel() as channel:
                queue = await channel.declare_queue(
                    queue_name,
                    durable=True,
                )
                await channel.default_exchange.publish(
                    aio_pika.Message(
                        body=message.model_dump_json().encode(),
                        delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                        content_type="application/json",
                    ),
                    routing_key=queue.name,
                )
        except (AMQPConnectionError, ChannelClosed) as e:
            logger.error("Publication error: %s", e)
            raise e
