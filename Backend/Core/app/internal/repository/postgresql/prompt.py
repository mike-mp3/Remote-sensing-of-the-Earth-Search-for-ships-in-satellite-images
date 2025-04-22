from typing import List

from app.internal.repository.postgresql.connection import get_connection
from app.internal.repository.postgresql.handlers.collect_response import (
    collect_response,
)
from app.internal.repository.repository import Repository
from app.pkg.models import CreatePromptCommand, Prompt, ReadPromptCommand
from app.pkg.models.app.prompts import (
    ReadPromptPageCommand,
    ReadPromptWithFilters,
    UpdatePromptStatusCommand,
)


class PromptRepository(Repository):
    @collect_response
    async def create(self, cmd: CreatePromptCommand) -> Prompt:
        q = """
            INSERT INTO prompts(user_id, prompt_id, raw_key)
            VALUES (
                %(user_id)s,
                %(prompt_id)s,
                %(raw_key)s
            )
            RETURNING
                id, user_id, prompt_id, raw_key,
                result_key, status, created_at, updated_at;
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()

    @collect_response
    async def update_status(self, cmd: UpdatePromptStatusCommand) -> Prompt:
        q = """
            UPDATE prompts
            SET
                result_key = %(result_key)s,
                status = %(status)s,
                updated_at = NOW()
            WHERE id = %(id)s
            RETURNING
                id, user_id, prompt_id, raw_key,
                result_key, status, created_at, updated_at;
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()

    @collect_response
    async def read(self, cmd: ReadPromptCommand) -> List[Prompt]:
        q = """
        SELECT
            id, user_id, prompt_id, raw_key,
            result_key, status, created_at, updated_at
        FROM prompts
        WHERE user_id = %(user_id)s
        ORDER BY created_at DESC, id DESC
        LIMIT %(size)s;
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchall()

    @collect_response
    async def read_page(self, cmd: ReadPromptPageCommand) -> List[Prompt]:
        q = """
            SELECT
                id, user_id, prompt_id, raw_key,
                result_key, status, created_at, updated_at
            FROM prompts
            WHERE
                user_id = %(user_id)s AND
                (created_at, id) < (%(created_at)s, %(prompt_id)s)
            ORDER BY created_at DESC, id DESC
            LIMIT %(size)s;
            """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchall()

    @collect_response
    async def read_with_filters(self, cmd: ReadPromptWithFilters) -> List[Prompt]:
        query = """
            SELECT
                id, user_id, prompt_id, raw_key,
                result_key, status, created_at, updated_at
            FROM prompts
            WHERE user_id = %(user_id)s
        """

        conditions = []

        if cmd.start_time:
            conditions.append("created_at >= %(start_time)s")
        if cmd.end_time:
            conditions.append("created_at <= %(end_time)s")
        if cmd.status:
            conditions.append("status = %(status)s")

        if conditions:
            query += " AND " + " AND ".join(conditions)

        query += " ORDER BY created_at DESC, id DESC"

        if cmd.limit:
            query += " LIMIT %(limit)s"
        else:
            query += " LIMIT ALL"

        async with get_connection() as cur:
            await cur.execute(query, cmd.to_dict())
            return await cur.fetchall()
