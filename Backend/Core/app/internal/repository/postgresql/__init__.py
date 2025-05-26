"""All postgresql repositories are defined here."""

from app.internal.repository.postgresql.prompt import PromptRepository
from app.internal.repository.postgresql.refresh_token import JWTRefreshTokenRepository
from app.internal.repository.postgresql.user import UserRepository
from dependency_injector import containers, providers


class Repositories(containers.DeclarativeContainer):
    """Container for postgresql repositories."""

    user_repository = providers.Factory(UserRepository)
    refresh_token_repository = providers.Factory(JWTRefreshTokenRepository)
    prompt_repository = providers.Factory(PromptRepository)
