"""
create-user-roles
"""

from yoyo import step

"""
add-user-roles
"""

from yoyo import step

steps = [
    step(
        """
        CREATE TABLE if NOT EXISTS user_roles (
            id serial PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL
        );

        INSERT INTO user_roles (name) VALUES 
            ('ADMIN'),
            ('DEFAULT');
        """,
        """
            DROP TABLE if EXISTS user_roles;
        """,
    ),
]
