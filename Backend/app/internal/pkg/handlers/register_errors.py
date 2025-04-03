from functools import wraps
from typing import Type
from app.pkg.models.base import BaseAPIException

# Global error registry for endpoints.
# This registry uses a unique key for each endpoint function,
# composed of the module and qualified name.
ERROR_REGISTRY = {}

def with_errors(*excs: Type[BaseAPIException]):
    """
    A decorator for registering errors associated with a specific endpoint.

    This decorator collects exception classes (which must inherit from BaseAPIException)
    and stores them in a global error registry using a unique key composed of the function's
    module and qualified name. This ensures that even if two functions have the same name
    in different modules, they are uniquely identified.

    Example usage:
        Suppose you have the following exception defined in your project:

            from app.pkg.models.base import BaseAPIException

            class UserNotActive(BaseAPIException):
                status_code = 403
                message = "User account is not active."

        And you define an endpoint function in the module "app.internal.routes.auth":

            @with_errors(UserNotActive)
            def login():
                # Your login logic here.
                pass

        In this case, the unique key for the function will be:
            "app.internal.routes.auth.login"
        And the error_registry will store the error response configuration as follows:

            {
                "app.internal.routes.auth.login": [
                    {
                        "status_code": 403,
                        "description": "User account is not active.",
                        "content": {
                            "application/json": {
                                "example": {"detail": "User account is not active."}
                            }
                        }
                    }
                ]
            }

    Returns:
        The original function, with its error configuration stored
        in the registry global container ERROR_REGISTRY.
    """

    def decorator(func):
        unique_key = f"{func.__module__}.{func.__qualname__}"
        ERROR_REGISTRY[unique_key] = [
            {
                "status_code": exc.status_code,
                "description": exc.message,
                "content": {
                    "application/json": {
                        "example": {"detail": exc.message}
                    }
                }
            }
            for exc in excs
        ]

        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
        return wrapper
    return decorator
