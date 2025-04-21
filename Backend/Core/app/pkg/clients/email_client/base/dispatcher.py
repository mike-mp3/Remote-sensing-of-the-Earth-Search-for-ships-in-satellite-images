from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from pydantic import EmailStr


class BaseEmailDispatcher(ABC):
    """Абстрактный класс для всех email_client-диспетчеров."""

    @abstractmethod
    async def send(
        self,
        to_email: EmailStr,
        subject: str,
        body: str,
        attachments: Optional[List[Tuple[bytes, str, str]]] = None,
    ):
        """Метод для отправки email_client."""
        pass
