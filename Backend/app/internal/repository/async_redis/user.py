from typing import Union

from app.internal.repository.async_redis.connection import get_connection
from app.internal.repository.repository import Repository
from app.pkg import models
from pydantic import SecretStr


class UserAsyncRedisRepository(Repository):
    """User repository implementation."""

    async def read(
        self,
        cmd: models.ReadUserConfirmationCode,
    ) -> Union[SecretStr | None]:
        async with get_connection() as connect:
            return SecretStr(await connect.get(cmd.email))

    async def create(self, cmd: models.CreateUserConfirmationCode) -> None:
        async with get_connection() as connect:
            return await connect.set(
                name=str(cmd.email),
                value=cmd.confirmation_code.get_secret_value(),
                ex=cmd.ex_time,
            )
