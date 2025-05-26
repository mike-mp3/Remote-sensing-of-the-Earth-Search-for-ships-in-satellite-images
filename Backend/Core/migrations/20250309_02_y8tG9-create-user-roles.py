"""
create-user-roles
"""

from yoyo import step

steps = [
    step(
        """
        CREATE TABLE if NOT EXISTS user_roles (
            id SMALLINT PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL
        );
        INSERT INTO user_roles (id, name) VALUES
            (1, 'ADMIN'),
            (2, 'DEFAULT')
        ON CONFLICT (id) DO UPDATE SET 
            name = EXCLUDED.name;     
        """,
        """
            DROP TABLE if EXISTS user_roles;
        """,
    ),
]
