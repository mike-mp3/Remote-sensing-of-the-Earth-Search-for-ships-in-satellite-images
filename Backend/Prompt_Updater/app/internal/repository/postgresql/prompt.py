from app.internal.repository.postgresql.connection import get_connection
from app.internal.repository.postgresql.handlers.collect_response import (
    collect_response,
)
from app.internal.repository.repository import Repository
from app.pkg.models import Prompt, UpdatePromptStatusCommand


class PromptRepository(Repository):
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
