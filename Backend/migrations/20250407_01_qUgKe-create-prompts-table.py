"""
create-prompts-table
"""

from yoyo import step

__depends__ = {'20250309_01_fkLwo-create-user-table'}

steps = [
    step(
        """
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'prompt_status') THEN
                CREATE TYPE prompt_status AS ENUM ('pending', 'success', 'error', 'cancelled');
            END IF;
        END$$;
        """,
        """
        DROP TYPE IF EXISTS prompt_status;
        """,
    ),
    step(
        """
        CREATE TABLE IF NOT EXISTS prompts (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id INTEGER NOT NULL REFERENCES users(id),
            prompt_id TEXT,
            raw_key TEXT NOT NULL,
            result_key TEXT,
            status prompt_status NOT NULL DEFAULT 'pending',
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW(),
            CONSTRAINT unique_user_prompt UNIQUE (user_id, prompt_id)
        );
        """,
        """
        DROP TABLE IF EXISTS prompts;
        """,
    ),
]
