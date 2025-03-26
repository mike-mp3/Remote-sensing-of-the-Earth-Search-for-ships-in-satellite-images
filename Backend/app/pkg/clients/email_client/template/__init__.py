from dependency_injector import containers, providers
from app.pkg.clients.email_client.template.confirmation import ConfirmationT
from ..base.template import BaseEmailTemplate

from ..dispatchers import Dispatchers

__all__ = [
    "Templates",
]

class Templates(containers.DeclarativeContainer):
    """Containers with services."""

    dispatchers = providers.Container(Dispatchers)

    user_confirmation: BaseEmailTemplate = providers.Singleton(
        ConfirmationT,
        dispatcher=dispatchers.smtp_dispatcher,
    )
