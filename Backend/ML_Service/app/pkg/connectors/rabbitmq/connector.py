import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import aio_pika
from aio_pika.exceptions import AMQPConnectionError
from app.pkg.logger import get_logger

__all__ = ["RabbitMQConnector"]

logger = get_logger(__name__)


class RabbitMQConnector:
    _connection: [aio_pika.RobustConnection, None]
    _channel_pool: [aio_pika.pool.Pool, None]

    _pool_size: int = 6
    _max_reconnect_attempts: int = 3
    _reconnect_delay: int = 10

    def __init__(self, dsn: str, heartbeat: int = 600):
        self.dsn = str(dsn)
        self.heartbeat = heartbeat
        self._connection = None
        self._channel = None

    async def connect(self):
        logger.debug("Trying to not native connect to RabbitMQ")
        reconnect_attempts = 0
        while True:
            try:
                self._connection = await aio_pika.connect_robust(
                    url=self.dsn,
                    heartbeat=self.heartbeat,
                )
                self._channel_pool = aio_pika.pool.Pool(
                    self._create_channel,
                    max_size=self._pool_size,
                )
                return
            except AMQPConnectionError as exc:
                reconnect_attempts += 1
                logger.error(
                    "Connection attempt %d/%d failed. Retrying after %ss...",
                    reconnect_attempts,
                    self._max_reconnect_attempts,
                    self._reconnect_delay,
                )
                error_msg = str(exc)
                if reconnect_attempts < self._max_reconnect_attempts:
                    await asyncio.sleep(self._reconnect_delay)
                else:
                    logger.error(f"Couldn't connect to RabbitMQ server. {error_msg}")
                    raise exc

    async def _create_channel(self):
        if self._connection and not self._connection.is_closed:
            channel = await self._connection.channel()
            await channel.set_qos(prefetch_count=1)
            return channel

    async def close_channel(self):
        if self._channel_pool is not None:
            await self._channel_pool.close()
            self._channel_pool = None

    async def close_connection(self):
        if self._connection and not self._connection.is_closed:
            await self._connection.close()
            self._connection = None

    @asynccontextmanager
    async def get_channel(self) -> AsyncGenerator[aio_pika.RobustChannel, None]:
        if not self._connection or self._connection.is_closed:
            await self.connect()
        async with self._channel_pool.acquire() as channel:
            yield channel
