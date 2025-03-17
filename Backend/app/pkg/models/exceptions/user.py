"""Exceptions for a User model."""

from starlette import status

from app.pkg.models.base import BaseAPIException

__all__ = [
    "UserAlreadyExists",
]

class UserAlreadyExists(BaseAPIException):
    message = "User already exists"
    status_code = status.HTTP_409_CONFLICT