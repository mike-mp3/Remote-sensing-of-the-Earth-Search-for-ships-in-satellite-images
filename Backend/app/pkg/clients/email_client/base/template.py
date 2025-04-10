from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import EmailStr

from .dispatcher import BaseEmailDispatcher

T = TypeVar("T", bound=BaseEmailDispatcher)


class BaseEmailTemplate(Generic[T], ABC):
    """Абстрактный класс для email_client-шаблонов."""

    @abstractmethod
    async def send(self, to_email: EmailStr, **kwargs):
        """Метод должен быть реализован в потомках."""
        pass
