"""Exceptions for token-based auth verification."""

from app.pkg.models.base import BaseAPIException
from starlette import status

__all__ = ["InvalidCredentials"]


class InvalidCredentials(BaseAPIException):
    message = "Could not validate credentials"
    status_code = status.HTTP_403_FORBIDDEN
