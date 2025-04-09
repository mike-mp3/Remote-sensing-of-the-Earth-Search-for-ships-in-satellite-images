"""Global point for collected routers. __routes__ is a :class:`.Routes`
instance that contains all routers in your application."""


from app.internal.routes import auth, prompt, user
from app.pkg.models.core.routes import Routes
from fastapi import APIRouter

__all__ = [
    "__routes__",
]

__routes__ = Routes(
    routers=(
        (
            user.router,
            auth.router,
            prompt.router,
        )
    ),
)
