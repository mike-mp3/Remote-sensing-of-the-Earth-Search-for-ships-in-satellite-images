"""
create-prompts-index-id-created-at
"""

from yoyo import step

__depends__ = {'20250407_01_qUgKe-create-prompts-table'}

steps = [
    step(
        """
        CREATE INDEX IF NOT EXISTS idx_prompts_created_at_id_desc 
        ON prompts (created_at DESC, id DESC)
        """,
        """
        DROP INDEX IF EXISTS idx_prompts_created_at_id_desc
        """,
    )
]
