import asyncio
import json
from typing import Any, Awaitable, Callable, Dict, Union

from aio_pika.abc import AbstractIncomingMessage, AbstractRobustQueue
from aio_pika.exceptions import AMQPConnectionError, ChannelClosed
from app.pkg.connectors.rabbitmq.connector import RabbitMQConnector
from app.pkg.logger import get_logger

logger = get_logger(__name__)


class RabbitMQConsumer:
    def __init__(self, connector: RabbitMQConnector):
        self.connector = connector

    async def consume_messages(
        self,
        queue_name: str,
        callback: Callable[[Dict], Union[Awaitable[None], Any]],
    ) -> None:
        try:
            async with self.connector.get_channel() as channel:
                logger.debug("Connected to RabbitMQ")
                queue: AbstractRobustQueue = await channel.declare_queue(
                    queue_name,
                    durable=True,
                )
                async with queue.iterator() as queue_iter:
                    async for message in queue_iter:
                        async with message.process():
                            await self._process_message(message, callback)

        except (AMQPConnectionError, ChannelClosed) as e:
            raise e from e
        except Exception as e:
            logger.error("Consuming error: %s", e)

    async def _process_message(
        self,
        message: AbstractIncomingMessage,
        callback: Callable[[Dict], Union[Awaitable[None], Any]],
    ):
        data = None
        try:
            data = self._parse_message_body(message.body)
        except ValueError as e:
            logger.warning(str(e))
        if data:
            try:
                result = callback(data)
                if asyncio.iscoroutine(result):
                    await result
            except Exception as e:
                logger.error("Error while processing message: %s", e)

    @staticmethod
    def _parse_message_body(body: bytes) -> Dict[str, Any]:
        """Convert message body to dictionary."""
        data = ""
        try:
            data = body.decode("utf-8")
            return json.loads(data)
        except (UnicodeDecodeError, json.JSONDecodeError):
            raise ValueError(f"Invalid message. Message: {data}")
