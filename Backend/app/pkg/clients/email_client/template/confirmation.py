from ..base.dispatcher import BaseEmailDispatcher
from ..base.template import BaseEmailTemplate, T
from pydantic import EmailStr, SecretStr


class ConfirmationT(BaseEmailTemplate[T]):
    """Класс для отправки email для подтверждения почты пользователя."""
    def __init__(self, dispatcher: BaseEmailDispatcher):
        self.dispatcher = dispatcher

    async def send(self, to_email: EmailStr, confirmation_code: SecretStr):
        subject = "Подтверждение почты"
        body = (f"Ваш код подтверждения: {confirmation_code.get_secret_value()}\n\n"
                f"Введите его в приложении для завершения регистрации.")
        await self.dispatcher.send(to_email, subject, body)
