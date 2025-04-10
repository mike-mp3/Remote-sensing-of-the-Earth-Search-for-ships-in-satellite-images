import asyncio
import inspect
import json
from typing import Any, Awaitable, Callable, Dict, Type, Union

import pydantic
from aio_pika.abc import AbstractIncomingMessage, AbstractRobustQueue
from aio_pika.exceptions import AMQPConnectionError, ChannelClosed
from app.pkg.connectors.rabbitmq.connector import RabbitMQConnector
from app.pkg.logger import get_logger
from app.pkg.models.base import BaseModel

logger = get_logger(__name__)

Callback = Callable[[BaseModel], Union[Awaitable[None], Any]]


class RabbitMQConsumer:
    def __init__(self, connector: RabbitMQConnector):
        self.connector = connector

    async def consume_messages(
        self,
        queue_name: str,
        callback: Callback,
    ) -> None:
        model_class = self._get_callback_model(callback)

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
                            await self._process_message(
                                message,
                                callback,
                                model_class,
                            )

        except (AMQPConnectionError, ChannelClosed) as e:
            raise e from e
        except Exception as e:
            logger.error("Consuming error: %s", e)

    async def _process_message(
        self,
        message: AbstractIncomingMessage,
        callback: Callback,
        model_class: Type[BaseModel],
    ):
        try:
            data: dict = self._parse_message_body(message.body)
        except ValueError as e:
            logger.warning(str(e))
            return

        try:
            model_instance = model_class(**data)
        except pydantic.ValidationError:
            logger.warning(
                "Validation error. Incoming data: %s. Expected fields: %s",
                data,
                list(model_class.model_fields.keys()),
            )
            return

        try:
            result = callback(model_instance)
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

    @staticmethod
    def _get_callback_model(callback: Callback) -> Type[BaseModel]:
        sig = inspect.signature(callback)
        params = list(sig.parameters.values())
        if not params:
            raise ValueError("Callback function must have at least one parameter")
        for param in params:
            if param.annotation is not inspect.Parameter.empty:
                model_class = param.annotation
                if not isinstance(model_class, type) or not issubclass(
                    model_class,
                    BaseModel,
                ):
                    raise ValueError(
                        "Annotation of callback parameter must be subclass of BaseModel",
                    )
                return model_class
        raise ValueError(
            "Callback function must have parameter with BaseModel type annotation",
        )
