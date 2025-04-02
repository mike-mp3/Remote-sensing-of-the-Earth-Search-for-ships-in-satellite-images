from app.pkg.logger import get_logger
from app.pkg.clients.email_client.base.dispatcher import BaseEmailDispatcher
from aiosmtplib import SMTP
from typing import Optional
from pydantic import EmailStr
from email.message import EmailMessage
import aiosmtplib

logger = get_logger(__name__)

# TODO: 1. реализовать сначала попытку use_tls, только потом start_tls
# TODO: 2. реализовать 2 сервер
# TODO: 3. MIMEText
class SMTPEmailDispatcher(BaseEmailDispatcher):
    def __init__(
            self,
            smtp_host: str,
            smtp_port: int,
            username: str,
            password: str,
            use_tls: bool,
            timeout: float = 30.0
    ):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.use_tls = use_tls
        self.timeout = timeout
        self._client: Optional[SMTP] = None

    def get_connection(self) -> SMTP:
        """Фабричный метод для создания SMTP-клиента"""
        return SMTP(
            hostname=self.smtp_host,
            port=self.smtp_port,
            username=self.username,
            password=self.password,
            use_tls=self.use_tls,
            timeout=self.timeout
        )

    # todo: добавить в body возможность приема SecretStr, SecretBytes
    # todo: а так же парсер body
    async def send(self, to_email: EmailStr, subject: str, body: str):
        async with self.get_connection() as conn:
            msg = EmailMessage()
            msg["From"] = self.username
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.set_content(body)

            try:
                await conn.send_message(msg)
                logger.info(f"Email was sent to {to_email}")
            except aiosmtplib.SMTPException as e:
                logger.error(f"SMTP error: {e}")
                raise e from Exception
            except Exception as e:
                logger.error(f"Failed to send email to {to_email}: {e}")