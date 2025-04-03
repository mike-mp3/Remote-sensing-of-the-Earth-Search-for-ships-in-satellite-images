from abc import ABC, abstractmethod
from pydantic import EmailStr

class BaseEmailDispatcher(ABC):
    """Абстрактный класс для всех email_client-диспетчеров."""

    @abstractmethod
    async def send(self, to_email: EmailStr, subject: str, body: str):
        """Метод для отправки email_client."""
        pass