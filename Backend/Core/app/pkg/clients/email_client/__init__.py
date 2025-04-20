from app.pkg.clients.email_client.client import EmailClient
from app.pkg.clients.email_client.dispatchers import Dispatchers
from dependency_injector import containers, providers

__all__ = ["Email", "EmailClient"]


class Email(containers.DeclarativeContainer):
    """Containers with services."""

    dispatchers = providers.Container(Dispatchers)

    client = providers.Singleton(
        EmailClient,
        dispatcher=dispatchers.smtp_dispatcher,
    )
