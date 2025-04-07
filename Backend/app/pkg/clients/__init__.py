from dependency_injector import containers, providers

from .email_client.template import Templates
from .s3 import S3Clients

__all__ = ["Clients"]


class Clients(containers.DeclarativeContainer):
    """Containers with services."""

    email: Templates = providers.Container(Templates)

    # http = providers.Container(...)

    s3: S3Clients = providers.Container(S3Clients)
