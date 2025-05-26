from app.pkg.models.app.user_roles import UserRoleEnum, UserRoleID, UserRoleName
from app.pkg.models.base import BaseModel
from pydantic import (
    EmailStr,
    Field,
    PositiveInt,
    SecretBytes,
    SecretStr,
    field_validator,
)

__all__ = [
    "UserFields",
    "ActiveUser",
]


# todo: добавить аннотации филдам
class UserFields:
    id = Field(
        description="User ID",
        examples=[1],
    )
    email = Field(
        description="User email",
        examples=["example@mail.com"],
    )
    role_id = Field(
        description="User role ID. 1 - ADMIN. 2 - DEFAULT",
        examples=[1],
    )
    role_name = Field(
        description="User role name. DEFAULT with regular access. "
        "ADMIN for all for all privileges",
        examples=["DEFAULT", "ADMIN"],
    )
    is_activated = Field(
        description="Has user confirmed his email",
        examples=["True", "False"],
    )


class BaseUser(BaseModel):
    """User base model"""


class ActiveUser(BaseUser):
    id: PositiveInt = UserFields.id
    email: EmailStr = UserFields.email
    role_name: UserRoleName = UserFields.role_name
    is_activated: bool = UserFields.is_activated
