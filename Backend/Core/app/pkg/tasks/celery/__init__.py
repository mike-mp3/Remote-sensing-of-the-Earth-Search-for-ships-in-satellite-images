from dependency_injector import containers, providers

from .email import EmailTasks

__all__ = ["Celery"]


class Celery(containers.DeclarativeContainer):
    email_tasks = providers.Factory(EmailTasks)
