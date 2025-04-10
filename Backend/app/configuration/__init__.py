"""Collect or build all requirements for startup server.

In this module, you can add all your middlewares, routes, dependencies,
etc.

Containers need for register all dependencies in ``FastAPI`` server. For
start building your application, you **MUST** call wire_packages.

Examples:
    When you're using containers without FastAPI::

        >>> __containers__.wire_packages()

    When you using ``FastAPI`` server, you **MUST** pass an argument
    application instance::

        >>> from fastapi import FastAPI
        >>> app = FastAPI()
        >>> __containers__.wire_packages(app=app)
"""

from app.internal.services import Services
from app.pkg.clients import Clients, RabbitMQClient
from app.pkg.connectors import AsyncRedis, Connectors, PostgresSQL, RabbitMQ
from app.pkg.models.core import Container, Containers
from app.pkg.models.core.containers import Resource
from app.pkg.utils.jwt import JWT

__all__ = ["__containers__"]


__containers__ = Containers(
    pkg_name=__name__,
    containers=[
        Container(container=Clients),
        Container(container=Services),
        Container(container=JWT),
        Container(container=RabbitMQClient),
        Resource(
            container=Connectors,
            depends_on=[
                Container(container=PostgresSQL),
                Container(container=AsyncRedis),
                Container(container=RabbitMQ),
            ],
        ),
    ],
)
