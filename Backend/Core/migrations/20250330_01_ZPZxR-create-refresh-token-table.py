"""
create-refresh-token-table
"""

from yoyo import step

__depends__ = {'20250309_01_fkLwo-create-user-table'}

steps = [
    step(
        """
            CREATE TABLE if NOT EXISTS refresh_tokens(
                id serial primary key, 
                user_id INT REFERENCES users(id),
                refresh_token text NOT NULL UNIQUE,
                constraint all_value_in_row_must_be_unique unique (
                    user_id, refresh_token
                )
            );
        """,
        """
            DROP TABLE if EXISTS refresh_tokens CASCADE;
        """,
    )
]
