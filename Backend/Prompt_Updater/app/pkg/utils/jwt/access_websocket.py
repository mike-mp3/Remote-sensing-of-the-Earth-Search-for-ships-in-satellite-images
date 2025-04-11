from datetime import timedelta
from typing import Optional, Set

from app.pkg.models.base import BaseAPIException
from app.pkg.models.exceptions.association.http_to_ws import Mapper
from app.pkg.utils.jwt.base import JwtAuthBase
from app.pkg.utils.jwt.credentionals import JwtAuthorizationCredentials
from fastapi import Security, WebSocketException
from jose import jwt
from pydantic import SecretStr

__all__ = ["JwtAccessWebSocketCookie"]


class JwtAccessWebsocket(JwtAuthBase):
    _cookie = JwtAuthBase.JwtAccessWebSocketCookie()

    def __init__(
        self,
        secret_key: SecretStr,
        places: Optional[Set[str]] = None,
        auto_error: bool = True,
        algorithm: str = jwt.ALGORITHMS.HS256,
        access_expires_delta: Optional[timedelta] = None,
        refresh_expires_delta: Optional[timedelta] = None,
    ):
        super().__init__(
            secret_key,
            places=places,
            auto_error=auto_error,
            algorithm=algorithm,
            access_expires_delta=access_expires_delta,
            refresh_expires_delta=refresh_expires_delta,
        )

    async def _get_credentials(
        self,
        cookie: Optional[JwtAuthBase.JwtAccessCookie],
    ) -> Optional[JwtAuthorizationCredentials]:
        payload, raw_token = await self._get_payload(
            bearer=None,
            cookie=cookie,
        )

        if payload:
            return JwtAuthorizationCredentials(
                subject=payload["subject"],
                raw_token=SecretStr(raw_token),
                jti=payload.get("jti", None),
            )
        return None


class JwtAccessWebSocketCookie(JwtAccessWebsocket):
    def __init__(
        self,
        secret_key: SecretStr,
        auto_error: bool = True,
        algorithm: str = jwt.ALGORITHMS.HS256,
        access_expires_delta: Optional[timedelta] = None,
        refresh_expires_delta: Optional[timedelta] = None,
    ):
        super().__init__(
            secret_key=secret_key,
            places={"cookie"},
            auto_error=auto_error,
            algorithm=algorithm,
            access_expires_delta=access_expires_delta,
            refresh_expires_delta=refresh_expires_delta,
        )

    async def __call__(
        self,
        cookie: JwtAuthBase.JwtAccessCookie = Security(JwtAccessWebsocket._cookie),
    ) -> Optional[JwtAuthorizationCredentials]:
        try:
            return await self._get_credentials(cookie=cookie)
        except BaseAPIException as exc:
            raise WebSocketException(
                code=Mapper.map_http_to_ws(exc.status_code),
                reason=exc.message,
            )
