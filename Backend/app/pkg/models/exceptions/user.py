"""Exceptions for a User model."""

from starlette import status

from app.pkg.models.base import BaseAPIException

__all__ = [
    "UserAlreadyExists",
    "IncorrectCode",
    "CodeNotFound",
    "TryToRegisterAgain"
]

class UserAlreadyExists(BaseAPIException):
    message = "User already exists"
    status_code = status.HTTP_409_CONFLICT

class TryToRegisterAgain(BaseAPIException):
    message = "User not found. Try again register again"
    status_code = status.HTTP_404_NOT_FOUND


class IncorrectCode(BaseAPIException):
    message = "Incorrect confirmation code"
    status_code = status.HTTP_400_BAD_REQUEST


# 1) Прошло слишком много времени, код пропал из редиса
# 2) Пользователь ввел не свой email
class CodeNotFound(BaseAPIException):
    message = "User confirmation code not found"
    status_code = status.HTTP_404_NOT_FOUND