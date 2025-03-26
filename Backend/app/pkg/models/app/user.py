from unittest.mock import DEFAULT

from app.pkg.models import UserRoleName
from app.pkg.models.app.user_roles import UserRoleEnum
from app.pkg.models.base import BaseModel
from pydantic import (
    Field,
    SecretStr,
    SecretBytes,
    EmailStr,
    PositiveInt,
    field_validator,
)

__all__ = [
    "User",
    "CreateUserRequest",
    "CreateUserCommand",
    "CreateUserResponse",
    "CreateUserConfirmationCode"
]

class UserFields:
    id = Field(
        description="User ID",
        examples=[1]
    )
    email = Field(
        description="User email",
        examples=["example@mail.com"]
    )
    role_id = Field(
        description="User role ID. 1 - ADMIN. 2 - DEFAULT",
        examples=[1]
    )
    role_name = Field(
        description="User role name. DEFAULT with regular access. ADMIN for all for all privileges",
        examples=["DEFAULT", "ADMIN"]
    )
    unencrypted_password = Field(
        description="User password must contain 6-64 symbols, minimum 1 uppercase letter and 1 digit",
        alias="password",
        min_length=6,
        max_length=64,
        examples=["SecurePass123"],
    )
    #todo: добавить поля в Field encrypted_password
    encrypted_password = Field(
        description="Encrypted user password"
    )
    is_activated = Field(
        description="Has user confirmed his email",
        examples=["True", "False"],
    )
    confirmation_code = Field(
        description="Confirmation email code",
        min_length=6,
        max_length=6,
        examples=["357298"],
    )

class BaseUser(BaseModel):
    """User base model"""


# Representation layer
class CreateUserRequest(BaseUser):
    email: EmailStr = UserFields.email
    password: SecretStr = UserFields.unencrypted_password

    @field_validator('password', mode="after")
    @classmethod
    def validate_password_complexity(cls, v: SecretStr) -> SecretStr:
        password = v.get_secret_value()

        if not any(c.isupper() for c in password):
            raise ValueError("Password must contain minimum 1 uppercase letter")

        if not any(c.isdigit() for c in password):
            raise ValueError("Password must contain minimum 1 digit")

        return v

class CreateUserResponse(BaseUser):
    email: EmailStr = UserFields.email
    role_name: UserRoleName = UserRoleEnum.DEFAULT.name


# Commands - SQL
class User(BaseUser):
    id: PositiveInt = UserFields.id
    email: EmailStr = UserFields.email
    role_id: PositiveInt = UserFields.role_id
    is_activated: bool = UserFields.is_activated
    password: SecretStr = UserFields.encrypted_password

class CreateUserCommand(BaseUser):
    email: EmailStr = UserFields.email
    password: SecretBytes = UserFields.encrypted_password


# Commands - NoSQL
class CreateUserConfirmationCode(BaseUser):
    email: EmailStr = UserFields.email
    confirmation_code: SecretStr = UserFields.confirmation_code