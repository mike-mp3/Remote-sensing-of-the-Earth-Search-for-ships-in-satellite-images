import asyncio
import functools
from typing import Any, Callable
from celery.signals import worker_process_init

from app.internal.repository.postgresql import Repository

__all__ = ["async_to_sync"]


@worker_process_init.connect
def init_celery_worker(**kwargs):
    """ Wire packages during worker initialization to inject dependencies. """
    from app.configuration import __containers__
    from app.pkg.models.core import Container

    # Добавляем репозиторий, чтобы мы могли его внедрять на уровне celery
    # (для приложения это не нужно)
    __containers__.containers.append(Container(container=Repository))
    __containers__.wire_packages()


def async_to_sync(task: Any) -> Callable[[Any], Any]:
    @functools.wraps(task)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return asyncio.run(
            task(*args, **kwargs)
        )
    return wrapper
