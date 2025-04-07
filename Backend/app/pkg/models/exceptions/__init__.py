"""All exceptions for the API you must store here.

Examples:
    This is a simple example of how to create an exception::
        >>> from app.pkg.models.base import BaseAPIException
        >>> from starlette import status
        >>> class MyException(BaseAPIException):
        ...     message = "My message"
        ...     status_code = status.HTTP_400_BAD_REQUEST
"""

from app.pkg.models.exceptions.user import (
    UserAlreadyExists,
    IncorrectCode,
    CodeNotFound,
    UserNotFound,
)

from app.pkg.models.exceptions.jwt import (
    UnAuthorized,
    TokenTimeExpired,
    WrongToken,
    IncorrectTokenPlace,
    AlgorithIsNotSupported,
)

from app.pkg.models.exceptions.auth import (
    IncorrectUsernameOrPassword,
    UserIsNotActivated,
)

from app.pkg.models.exceptions.prompt import (
    InvalidPromptPath,
    RawPromptNowFound,
    RawPromptAlreadyExists,
)