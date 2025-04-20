from app.pkg.clients.email_client.base.dispatcher import BaseEmailDispatcher
from pydantic import EmailStr, SecretStr


class EmailClient:
    def __init__(self, dispatcher: BaseEmailDispatcher):
        self.dispatcher = dispatcher

    async def send_confirmation(self, to_email: EmailStr, confirmation_code: str):
        subject = "Подтверждение почты"
        body = (
            f"Ваш код подтверждения: {confirmation_code}\n\n"
            f"Введите его в приложении для завершения регистрации."
        )
        await self.dispatcher.send(to_email, subject, body)
