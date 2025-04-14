from functools import wraps

from app.pkg import models
from app.pkg.models.exceptions.jwt import (
    TokenTimeExpired,
    UnAuthorized,
    WrongToken,
)
from app.pkg.settings import settings
from dependency_injector import containers, providers
from dependency_injector.providers import Factory
from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Security

from .access import JwtAccessCookie
from .credentionals import JwtAuthorizationCredentials
from .refresh import JwtRefreshCookie

__all__ = [
    "JWT",
    "JwtAuthorizationCredentials",
    "JwtAccessCookie",
    "JwtRefreshCookie",
    "access_security",
    "refresh_security",
    "update_jwt",
    "UnAuthorized",
    "TokenTimeExpired",
    "WrongToken",
    "get_current_user",
]


access_security = JwtAccessCookie(secret_key=settings.JWT.SECRET_KEY)
refresh_security = JwtRefreshCookie(secret_key=settings.JWT.SECRET_KEY)


class JWT(containers.DeclarativeContainer):
    access: Factory[JwtAccessCookie] = providers.Factory(
        JwtAccessCookie,
        secret_key=settings.JWT.SECRET_KEY,
    )
    refresh: Factory[JwtRefreshCookie] = providers.Factory(
        JwtRefreshCookie,
        secret_key=settings.JWT.SECRET_KEY,
    )


def update_jwt(func):
    @wraps(func)
    @inject
    async def wrapper(
        access_token: JwtAccessCookie = Depends(Provide[JWT.access]),
        *args,
        **kwargs,
    ):
        response = kwargs["response"]
        credentials = kwargs["credentials"]
        user_id = credentials.subject.get("user_id")
        user = await func(*args, **kwargs)
        if user.id != user_id:  # если айди не текущего пользователя, то не обновляем токен
            return user
        at = access_token.create_access_token(
            subject={
                "user_id": user.id,
                "role_name": user.role_name,
                "departments_name": user.departments_name,
                "current_department": user.current_department_name,
                "username": user.username,
                "created_at": user.created_at.timestamp(),
            },
        )
        access_token.set_account_cookie(response=response, access_token=at)
        return user

    return wrapper


def get_current_user(
    jwt: JwtAuthorizationCredentials = Security(access_security),
) -> models.ActiveUser:
    return jwt.get_user()
