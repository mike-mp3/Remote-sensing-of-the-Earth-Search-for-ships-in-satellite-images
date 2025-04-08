import aio_pika
from aio_pika.exceptions import AMQPConnectionError, ChannelClosed

from app.pkg.connectors.rabbitmq.connector import RabbitMQConnector
from app.pkg.models.base import BaseModel
from app.pkg.logger import get_logger

__all__ = ['RabbitMQProducer']

logger = get_logger(__name__)


class RabbitMQProducer:

    def __init__(self, connector: RabbitMQConnector):
        self.conn = connector

    async def publish_message(self, message: BaseModel, queue_name: str):
        if not self.conn.connection or self.conn.connection.is_closed:
            await self.conn.connect()
        if not self.conn.channel or self.conn.channel.is_closed:
            await self.conn.open_channel()
        try:
            queue = await self.conn.channel.declare_queue(
                queue_name,
                durable=True,
            )
            await self.conn.channel.default_exchange.publish(
                aio_pika.Message(
                    body=message.model_dump_json().encode(),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                    content_type="application/json"
                ),
                routing_key=queue.name
            )
        except (AMQPConnectionError, ChannelClosed) as e:
            logger.error("Publication error: %s", e)
            raise e

