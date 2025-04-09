import asyncio

import aio_pika
from aio_pika.exceptions import AMQPConnectionError
from app.pkg.logger import get_logger

__all__ = ["RabbitMQConnector"]

logger = get_logger(__name__)


class RabbitMQConnector:
    _connection: [aio_pika.RobustConnection, None]
    _channel: [aio_pika.RobustChannel, None]

    _reconnect_attempts = 0
    _max_reconnect_attempts = 3
    _reconnect_delay = 10

    def __init__(self, dsn: str, heartbeat: int = 600):
        self.dsn = str(dsn)
        self.heartbeat = heartbeat
        self._connection = None
        self._channel = None

    @property
    def connection(self) -> aio_pika.RobustConnection:
        return self._connection

    @property
    def channel(self) -> aio_pika.RobustChannel:
        return self._channel

    async def connect(self):
        print("AHHAHAHA я коннекчусь бро в коннекторе")
        error_msg = ""
        while True:
            try:
                self._connection = await aio_pika.connect_robust(
                    url=self.dsn,
                    heartbeat=self.heartbeat,
                )
                await self.open_channel()
                self._reconnect_attempts = 0
                return
            except AMQPConnectionError as exc:
                self._reconnect_attempts += 1
                logger.error(
                    "Connection attempt %d/%d failed. Retrying after %ss...",
                    self._reconnect_attempts,
                    self._max_reconnect_attempts,
                    self._reconnect_delay,
                )
                error_msg = str(exc)
                if self._reconnect_attempts < self._max_reconnect_attempts:
                    await asyncio.sleep(self._reconnect_delay)
                else:
                    logger.error(f"Couldn't connect to RabbitMQ server. {error_msg}")
                    raise exc

    async def open_channel(self):
        if self._connection and not self._connection.is_closed:
            self._channel = await self._connection.channel()
            await self._channel.set_qos(prefetch_count=1)

    async def close_channel(self):
        if self._channel and not self._channel.is_closed:
            await self._channel.close()
            self._channel = None

    async def close_connection(self):
        if self._connection and not self._connection.is_closed:
            await self._connection.close()
            self._connection = None
