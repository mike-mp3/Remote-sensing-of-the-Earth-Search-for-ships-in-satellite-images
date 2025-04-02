from fastapi import status

from app.pkg.models.base import BaseAPIException

__all__ = [
    "UnAuthorized",
    "TokenTimeExpired",
    "WrongToken",
    "IncorrectTokenPlace",
    "AlgorithIsNotSupported",
]


class UnAuthorized(BaseAPIException):
    message = "Not authorized"
    status_code = status.HTTP_401_UNAUTHORIZED


class TokenTimeExpired(BaseAPIException):
    message = "Token time expired"
    status_code = status.HTTP_401_UNAUTHORIZED


class IncorrectTokenPlace(BaseAPIException):
    message = "Only 'header'/'cookie' are supported"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class AlgorithIsNotSupported(BaseAPIException):
    message = "Algorithm is not supported"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class WrongToken(BaseAPIException):
    message = "Wrong token"
    status_code = status.HTTP_401_UNAUTHORIZED

