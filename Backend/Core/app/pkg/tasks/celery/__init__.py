from dependency_injector import containers, providers

from .email import EmailTasks
from .prompt import PromptTasks

__all__ = ["Celery", "EmailTasks", "PromptTasks"]


class Celery(containers.DeclarativeContainer):
    email_tasks = providers.Factory(EmailTasks)
    prompt_tasks = providers.Factory(
        PromptTasks
    )
