from app.pkg.clients.email_client.dispatchers.dispatcher_smtp import SMTPEmailDispatcher
from app.pkg.settings import settings
from dependency_injector import containers, providers

__all__ = ["Dispatchers"]


class Dispatchers(containers.DeclarativeContainer):
    """Containers with services."""

    smtp_dispatcher = providers.Singleton(
        SMTPEmailDispatcher,
        smtp_host=settings.SMTP.HOST,
        smtp_port=settings.SMTP.PORT,
        username=settings.SMTP.USERNAME,
        password=settings.SMTP.PASSWORD.get_secret_value(),
        use_tls=settings.SMTP.USE_TLS,
    )
