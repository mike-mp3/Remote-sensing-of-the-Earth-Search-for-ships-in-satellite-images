from typing import Optional

from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.security.api_key import APIKeyBase
from starlette.exceptions import WebSocketException
from starlette.status import WS_1008_POLICY_VIOLATION
from starlette.websockets import WebSocket
from typing_extensions import Annotated, Doc

__all__ = ["APIKeyWebSocketCookie"]


class APIKeyWebSocketCookie(APIKeyBase):
    def __init__(
        self,
        *,
        name: Annotated[str, Doc("Cookie name.")],
        scheme_name: Annotated[
            Optional[str],
            Doc(
                """
                Security scheme name.

                It will be included in the generated OpenAPI (e.g. visible at `/docs`).
                """,
            ),
        ] = None,
        description: Annotated[
            Optional[str],
            Doc(
                """
                Security scheme description.

                It will be included in the generated OpenAPI (e.g. visible at `/docs`).
                """,
            ),
        ] = None,
        auto_error: Annotated[
            bool,
            Doc(
                """
                By default, if the cookie is not provided, `APIKeyCookie` will
                automatically cancel the request and send the client an error.

                If `auto_error` is set to `False`, when the cookie is not available,
                instead of erroring out, the dependency result will be `None`.

                This is useful when you want to have optional authentication.

                It is also useful when you want to have authentication that can be
                provided in one of multiple optional ways (for example, in a cookie or
                in an HTTP Bearer token).
                """,
            ),
        ] = True,
    ):
        self.model = APIKey(
            **{"in": APIKeyIn.cookie},
            name=name,
            description=description,
        )
        self.scheme_name = scheme_name or self.__class__.__name__
        self.auto_error = auto_error
        self.description = description

    async def __call__(self, websocket: WebSocket) -> Optional[str]:
        api_key = websocket.cookies.get(self.model.name)
        if not api_key:
            if self.auto_error:
                raise WebSocketException(
                    code=WS_1008_POLICY_VIOLATION,
                    reason="Not authenticated: API key cookie is missing.",
                )
            else:
                return None
        return api_key
