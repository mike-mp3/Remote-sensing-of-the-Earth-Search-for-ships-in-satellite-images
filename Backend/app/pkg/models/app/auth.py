from app.pkg.models.app.jwt import JWTFields
from app.pkg.models.base import BaseModel
from app.pkg.models.app.user import UserFields

from pydantic import SecretStr, EmailStr

__all__ = [
    "AuthRequest",
]

class AuthFields:
    access_token: JWTFields.access_token
    refresh_token = JWTFields.refresh_token
    role_name = UserFields.role_name
    email = UserFields.email
    password = UserFields.unencrypted_password


class BaseAuth(BaseModel):
    """Base model for auth."""


# Representation layer
class AuthRequest(BaseAuth):
    email: EmailStr = AuthFields.email
    password: SecretStr = AuthFields.password



