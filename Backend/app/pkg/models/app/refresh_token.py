from pydantic import PositiveInt, SecretStr

from app.pkg.models.app.jwt import JWTFields
from app.pkg.models.app.user import UserFields
from app.pkg.models.base import BaseModel

__all__ = [
    "JWTFields",
    "JWTRefreshToken",
    "CreateJWTRefreshTokenCommand",
    "ReadJWTRefreshTokenQuery",
    "UpdateJWTRefreshTokenCommand",
    "DeleteJWTRefreshTokenCommand",
    "CreateOrUpdateJWTRefreshTokenCommand"
]


class JWTRefreshFields:
    user_id: PositiveInt = UserFields.id
    refresh_token: SecretStr = JWTFields.refresh_token


class BaseJWTRefreshToken(BaseModel):
    """Base class for refresh token."""

# From database
class JWTRefreshToken(BaseJWTRefreshToken):
    user_id: PositiveInt = JWTRefreshFields.user_id
    refresh_token: SecretStr = JWTRefreshFields.refresh_token


# Commands
class CreateJWTRefreshTokenCommand(BaseJWTRefreshToken):
    user_id: PositiveInt = JWTRefreshFields.user_id
    refresh_token: SecretStr = JWTRefreshFields.refresh_token


class UpdateJWTRefreshTokenCommand(BaseJWTRefreshToken):
    user_id: PositiveInt = JWTRefreshFields.user_id
    refresh_token: SecretStr = JWTRefreshFields.refresh_token

class CreateOrUpdateJWTRefreshTokenCommand(BaseJWTRefreshToken):
    user_id: PositiveInt = JWTRefreshFields.user_id
    refresh_token: SecretStr = JWTRefreshFields.refresh_token


class DeleteJWTRefreshTokenCommand(BaseJWTRefreshToken):
    user_id: PositiveInt = JWTRefreshFields.user_id
    refresh_token: SecretStr = JWTRefreshFields.refresh_token


# Queries
class ReadJWTRefreshTokenQuery(BaseJWTRefreshToken):
    user_id: PositiveInt = JWTRefreshFields.user_id
    refresh_token: SecretStr = JWTRefreshFields.refresh_token


