import asyncio
from functools import wraps
from typing import Any, Callable

from app.internal.repository.postgresql import Repositories
from celery.signals import worker_process_init

__all__ = ["async_to_sync"]


@worker_process_init.connect
def init_celery_worker(**kwargs):
    """Wire packages during worker initialization to inject dependencies."""
    from app.configuration import __containers__
    from app.pkg.models.core import Container

    __containers__.containers.append(Container(container=Repositories))
    __containers__.wire_packages()


def async_to_sync(task: Any) -> Callable[[Any], Any]:
    @wraps(task)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return asyncio.run(
            task(*args, **kwargs),
        )

    return wrapper
