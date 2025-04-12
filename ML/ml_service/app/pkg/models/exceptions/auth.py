from app.pkg.models.base import BaseAPIException
from fastapi import status

__all__ = [
    "IncorrectUsernameOrPassword",
    "UserIsNotActivated",
]


class IncorrectUsernameOrPassword(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Incorrect username or password"


class UserIsNotActivated(BaseAPIException):
    status_code = status.HTTP_403_FORBIDDEN
    message = "The user's identity has not been confirmed"
