"""Abstract connector.

Notes:
    All connectors must be inherited by :class:`.BaseConnector` and implement
        its method.
"""

from abc import abstractmethod
from contextlib import asynccontextmanager

__all__ = ["BaseConnector"]


class BaseConnector:
    """Abstract connector."""

    @abstractmethod
    @asynccontextmanager
    async def get_connect(self):
        """Getting connection pool in asynchronous context."""
        try:
            yield
        finally:
            raise NotImplementedError
