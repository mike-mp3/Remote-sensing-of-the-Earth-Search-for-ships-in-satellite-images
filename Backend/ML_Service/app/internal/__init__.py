from app.internal.services import Services
from app.pkg.clients import Clients, RabbitMQClient
from app.pkg.connectors import Connectors, RabbitMQ
from app.pkg.models.core import Container, Containers
from app.pkg.models.core.containers import Resource

__all__ = ["__containers__"]


__containers__ = Containers(
    pkg_name=__name__,
    containers=[
        Container(container=Clients),
        Container(container=Services),
        Container(container=RabbitMQClient),
        Resource(
            container=Connectors,
            depends_on=[
                Container(container=RabbitMQ),
            ],
        ),
    ],
)
