"""All postgresql repositories are defined here."""

from app.internal.repository.postgresql.prompt import PromptRepository
from dependency_injector import containers, providers


class Repositories(containers.DeclarativeContainer):
    """Container for postgresql repositories."""

    prompt_repository = providers.Factory(PromptRepository)
