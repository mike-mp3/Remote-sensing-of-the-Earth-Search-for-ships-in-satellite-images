from contextlib import asynccontextmanager
from typing import AsyncGenerator

from app.pkg.connectors import Connectors
from app.pkg.connectors.async_redis import AsyncRedis
from dependency_injector.wiring import Provide, inject
from redis.asyncio import Redis


@asynccontextmanager
@inject
async def get_connection(
    redis_connector: AsyncRedis = Provide[Connectors.async_redis.connector],
) -> AsyncGenerator[Redis, None]:
    async with redis_connector.get_connect() as conn:
        yield conn
