from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

from redis.asyncio import ConnectionPool, Redis

from ..connector import BaseConnector

__all__ = ["AsyncRedisConnector"]


class AsyncRedisConnector(BaseConnector):
    _pool: Optional[ConnectionPool] = None

    def __init__(self, dsn: str):
        self.dsn = str(dsn)

    @asynccontextmanager
    async def get_connect(self) -> AsyncGenerator[Redis, None]:
        """Connection with pool"""
        if self._pool is None:
            self._pool = ConnectionPool.from_url(
                self.dsn,
                decode_responses=True,
                socket_connect_timeout=5,
            )
        client = Redis(
            connection_pool=self._pool,
            auto_close_connection_pool=False,
        )
        try:
            yield client
        finally:
            await client.close()
