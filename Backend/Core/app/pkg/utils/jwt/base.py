from abc import ABC
from datetime import UTC, datetime, timedelta
from typing import Any, Dict, Optional, Set, Tuple
from uuid import uuid4

from app.pkg.models.exceptions.jwt import (
    AlgorithIsNotSupported,
    IncorrectTokenPlace,
    TokenTimeExpired,
    UnAuthorized,
    WrongToken,
)
from app.pkg.settings import settings
from fastapi.responses import Response
from fastapi.security import APIKeyCookie, HTTPBearer
from jose import jwt
from pydantic import SecretStr

__all__ = ["JwtAuthBase"]


class JwtAuthBase(ABC):
    class JwtAccessCookie(APIKeyCookie):
        def __init__(self, *args: Any, **kwargs: Any):
            APIKeyCookie.__init__(
                self,
                *args,
                name=settings.JWT.ACCESS_TOKEN_NAME,
                auto_error=False,
                **kwargs,
            )

    class JwtRefreshCookie(APIKeyCookie):
        def __init__(self, *args: Any, **kwargs: Any):
            APIKeyCookie.__init__(
                self,
                *args,
                name=settings.JWT.REFRESH_TOKEN_NAME,
                auto_error=False,
                **kwargs,
            )

    class JwtAccessBearer(HTTPBearer):
        def __init__(self, *args: Any, **kwargs: Any):
            HTTPBearer.__init__(self, *args, auto_error=False, **kwargs)

    class JwtRefreshBearer(HTTPBearer):
        def __init__(self, *args: Any, **kwargs: Any):
            HTTPBearer.__init__(self, *args, auto_error=False, **kwargs)

    def __init__(
        self,
        secret_key: SecretStr,
        places: Optional[Set[str]] = None,
        auto_error: bool = True,
        algorithm: jwt.ALGORITHMS = jwt.ALGORITHMS.HS256,
        access_expires_delta: Optional[timedelta] = None,
        refresh_expires_delta: Optional[timedelta] = None,
    ):
        if places:
            if not places.issubset({"header", "cookie"}):
                raise IncorrectTokenPlace
        algorithm = algorithm.upper()
        if not hasattr(jwt.ALGORITHMS, algorithm):
            raise AlgorithIsNotSupported

        self.secret_key = secret_key

        self.places = places or {"header"}
        self.auto_error = auto_error
        self.algorithm = algorithm
        self.access_expires_delta = access_expires_delta or timedelta(hours=6)
        self.refresh_expires_delta = refresh_expires_delta or timedelta(days=30)

    @classmethod
    def from_other(
        cls,
        other: "JwtAuthBase",
        secret_key: Optional[SecretStr] = None,
        auto_error: Optional[bool] = None,
        algorithm: Optional[str] = None,
        access_expires_delta: Optional[timedelta] = None,
        refresh_expires_delta: Optional[timedelta] = None,
    ) -> "JwtAuthBase":
        return cls(
            secret_key=secret_key or other.secret_key,
            auto_error=auto_error or other.auto_error,
            algorithm=algorithm or other.algorithm,
            access_expires_delta=access_expires_delta or other.access_expires_delta,
            refresh_expires_delta=refresh_expires_delta or other.refresh_expires_delta,
        )

    def _decode_payload(self, token: SecretStr) -> Optional[Dict[str, Any]]:
        try:
            payload: Dict[str, Any] = jwt.decode(
                token.get_secret_value(),
                self.secret_key.get_secret_value(),
                algorithms=[self.algorithm],
                options={"leeway": 10},
            )
        except jwt.ExpiredSignatureError:
            if self.auto_error:
                raise TokenTimeExpired
            else:
                return None
        except jwt.JWTError:
            if self.auto_error:
                raise WrongToken
            else:
                return None
        else:
            return payload

    async def _get_payload(
        self,
        bearer: Optional[HTTPBearer],
        cookie: Optional[APIKeyCookie],
    ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        token: Optional[str] = None
        if bearer:
            token = str(bearer.credentials)  # type: ignore
        elif cookie:
            token = str(cookie)

        if not token:
            if self.auto_error:
                raise UnAuthorized
            else:
                return None, None

        payload = self._decode_payload(SecretStr(token))
        return payload, token

    @staticmethod
    def _generate_payload(
        subject: Dict[str, Any],
        expires_delta: timedelta,
        unique_identifier: str,
        token_type: str,
    ) -> Dict[str, Any]:

        now = datetime.now(UTC)
        return {
            "subject": subject.copy(),  # main subject
            "type": token_type,  # 'access' or 'refresh' token
            "exp": now + expires_delta,  # expire time
            "iat": now,  # creation time
            "jti": unique_identifier,  # uuid
        }

    def create_access_token(
        self,
        subject: Dict[str, Any],
        expires_delta: Optional[timedelta] = None,
        unique_identifier: Optional[str] = None,
    ) -> str:
        expires_delta = expires_delta or self.access_expires_delta
        unique_identifier = unique_identifier or str(uuid4())
        to_encode = self._generate_payload(
            subject,
            expires_delta,
            unique_identifier,
            "access",
        )
        jwt_encoded: str = jwt.encode(
            to_encode,
            self.secret_key.get_secret_value(),
            algorithm=self.algorithm,
        )
        return jwt_encoded

    def create_refresh_token(
        self,
        subject: Dict[str, Any],
        expires_delta: Optional[timedelta] = None,
        unique_identifier: Optional[str] = None,
    ) -> str:
        expires_delta = expires_delta or self.refresh_expires_delta
        unique_identifier = unique_identifier or str(uuid4())
        to_encode = self._generate_payload(
            subject,
            expires_delta,
            unique_identifier,
            "refresh",
        )
        jwt_encoded: str = jwt.encode(
            to_encode,
            self.secret_key.get_secret_value(),
            algorithm=self.algorithm,
        )
        return jwt_encoded

    @staticmethod
    def set_refresh_cookie(
        response: Response,
        refresh_token: str,
        expires_delta: Optional[timedelta] = None,
    ) -> None:
        seconds_expires: Optional[int] = (
            int(expires_delta.total_seconds()) if expires_delta else None
        )
        response.set_cookie(
            key=settings.JWT.REFRESH_TOKEN_NAME,
            value=refresh_token,
            httponly=True,
            max_age=seconds_expires,
            samesite="none",
            secure=True,  # type: ignore
        )

    @staticmethod
    def set_account_cookie(
        response: Response,
        access_token: str,
        expires_delta: Optional[timedelta] = None,
    ) -> None:
        seconds_expires: Optional[int] = (
            int(expires_delta.total_seconds()) if expires_delta else None
        )
        response.set_cookie(
            key=settings.JWT.ACCESS_TOKEN_NAME,
            value=access_token,
            httponly=True,
            max_age=seconds_expires,
            samesite="none",
            secure=True,  # type: ignore
        )

    @staticmethod
    def unset_refresh_cookie(response: Response) -> None:
        response.delete_cookie(
            key=settings.JWT.REFRESH_TOKEN_NAME,
            httponly=True,
        )
