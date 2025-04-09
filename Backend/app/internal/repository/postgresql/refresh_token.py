from app.internal.repository.postgresql.connection import get_connection
from app.internal.repository.postgresql.handlers.collect_response import (
    collect_response,
)
from app.internal.repository.repository import Repository
from app.pkg.models import (
    CreateJWTRefreshTokenCommand,
    DeleteJWTRefreshTokenCommand,
    JWTRefreshToken,
    ReadJWTRefreshTokenQuery,
    UpdateJWTRefreshTokenCommand,
)


class JWTRefreshTokenRepository(Repository):
    @collect_response
    async def create(self, cmd: CreateJWTRefreshTokenCommand) -> JWTRefreshToken:
        q = """
            INSERT INTO refresh_tokens(user_id, refresh_token)
                VALUES (%(user_id)s, %(refresh_token)s)
            RETURNING user_id, refresh_token;
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict(show_secrets=True))
            return await cur.fetchone()

    @collect_response
    async def read(self, query: ReadJWTRefreshTokenQuery) -> JWTRefreshToken:
        q = """
            SELECT user_id, refresh_token
                FROM refresh_tokens
            WHERE user_id = %(user_id)s AND refresh_token = %(refresh_token)s;
        """
        async with get_connection() as cur:
            await cur.execute(q, query.to_dict(show_secrets=True))
            return await cur.fetchone()

    @collect_response
    async def update(self, cmd: UpdateJWTRefreshTokenCommand) -> JWTRefreshToken:
        q = """
            UPDATE refresh_tokens SET refresh_token = %(refresh_token)s
                WHERE user_id = %(user_id)s
            RETURNING user_id, refresh_token;
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict(show_secrets=True))
            return await cur.fetchone()

    @collect_response
    async def delete(self, cmd: DeleteJWTRefreshTokenCommand) -> JWTRefreshToken:
        q = """
            DELETE FROM refresh_tokens
                WHERE user_id = %(user_id)s
            RETURNING user_id, refresh_token;
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict(show_secrets=True))
            return await cur.fetchone()
