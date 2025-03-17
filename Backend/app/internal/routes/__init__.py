"""Global point for collected routers. __routes__ is a :class:`.Routes`
instance that contains all routers in your application."""


from fastapi import APIRouter

from app.pkg.models.core.routes import Routes
from app.internal.routes import (
    user
)

__all__ = [
    "__routes__",
]

__routes__ = Routes(
    routers=(
        (
            user.router,
        )
    ),
)
