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
                role_id int NOT NULL REFERENCES user_roles(id),
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
        """,
        """
            DROP TABLE if EXISTS users;
        """,
    ),
]
