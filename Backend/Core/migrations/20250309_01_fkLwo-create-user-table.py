"""
create-user-table
"""

from yoyo import step

__depends__ = {'20250309_02_y8tG9-create-user-roles'}

steps = [
    step(
        """
            CREATE TABLE if NOT EXISTS users (
                id serial PRIMARY KEY,
                email text UNIQUE NOT NULL,
                password bytea NOT NULL,
                role_id smallint NOT NULL REFERENCES user_roles(id) DEFAULT 2,
                is_activated boolean NOT NULL DEFAULT FALSE,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
        """,
        """
            DROP TABLE if EXISTS users;
        """,
    ),
]
