import logging

from app.internal.repository.postgresql.connection import get_connection
from app.internal.repository.postgresql.handlers.collect_response import (
    collect_response,
)
from app.internal.repository.repository import Repository
from app.pkg import models

__all__ = ["UserRepository"]

logger = logging.getLogger(__name__)


class UserRepository(Repository):
    """User repository implementation."""

    @collect_response
    async def create(self, cmd: models.CreateUserCommand) -> models.User:
        q = """
            INSERT INTO users (email, password)
                VALUES (%(email)s, %(password)s)
            RETURNING
                id, email, role_id, is_activated, password
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict(show_secrets=True))
            return await cur.fetchone()

    @collect_response
    async def upsert_inactive_user(self, cmd: models.CreateUserCommand) -> models.User:
        q = """
        INSERT INTO users (email, password)
            VALUES (%(email)s, %(password)s)
        ON CONFLICT (email) DO UPDATE SET
            password=EXCLUDED.password,
            created_at=NOW()
        WHERE
            users.is_activated = false
        RETURNING
            id, email, role_id, is_activated, password
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict(show_secrets=True))
            return await cur.fetchone()

    @collect_response
    async def read_by_email(
        self,
        cmd: models.ReadUserByEmailCommand,
    ) -> models.User:
        q = """
            SELECT id, email, role_id, is_activated, password
                FROM users
            WHERE email = %(email)s
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()

    @collect_response
    async def update_user_status(
        self,
        cmd: models.UpdateUserStatusCommand,
    ) -> models.User:
        q = """
            UPDATE users
                SET is_activated = %(is_activated)s
            WHERE email = %(email)s AND is_activated <> %(is_activated)s
            RETURNING
                id, email, role_id, is_activated, password;
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()
