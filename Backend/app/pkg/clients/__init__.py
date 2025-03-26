from dependency_injector import containers, providers

from .email_client.template import Templates

__all__ = ["Clients"]

class Clients(containers.DeclarativeContainer):
    """Containers with services."""

    email: Templates = providers.Container(Templates)

    # http = providers.Container(...)


