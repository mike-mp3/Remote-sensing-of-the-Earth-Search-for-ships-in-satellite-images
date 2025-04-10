from app.pkg.connectors.resources import BaseAsyncResource
from app.pkg.logger import get_logger

from .connector import RabbitMQConnector

logger = get_logger(__name__)

__all__ = ["RabbitMQResource"]


class RabbitMQResource(BaseAsyncResource):
    def __init__(self, connector: RabbitMQConnector):
        self.connector = connector

    async def init(self, *args, **kwargs) -> "RabbitMQResource":
        await self.connector.connect()
        return self

    async def shutdown(self, resource: "RabbitMQResource"):
        await resource.connector.close_channel()
        await resource.connector.close_connection()
