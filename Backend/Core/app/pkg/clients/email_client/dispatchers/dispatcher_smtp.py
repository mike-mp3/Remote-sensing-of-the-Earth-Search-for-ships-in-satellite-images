from email.message import EmailMessage
from typing import List, Optional, Tuple

import aiosmtplib
from aiosmtplib import SMTP
from app.pkg.clients.email_client.base.dispatcher import BaseEmailDispatcher
from app.pkg.logger import get_logger
from pydantic import EmailStr

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
        timeout: float = 30.0,
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
            timeout=self.timeout,
        )

    async def __send_message(self, msg: EmailMessage) -> None:
        async with self.get_connection() as conn:
            try:
                await conn.send_message(msg)
            except aiosmtplib.SMTPException as e:
                logger.error("SMTP error: %s", e)
                raise e from e
            except Exception as e:
                to = msg.get("To")
                logger.error("Failed to send email to %s: %s", to, e)

    # todo: добавить в body возможность приема SecretStr, SecretBytes
    # todo: а так же парсер body
    async def send(
        self,
        to_email: EmailStr,
        subject: str,
        body: str,
        attachments: Optional[List[Tuple[bytes, str, str]]] = None,
    ):
        msg = EmailMessage()
        msg["From"] = self.username
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body)

        if attachments:
            for data, mime_type, filename in attachments:
                maintype, subtype = mime_type.split("/", 1)
                msg.add_attachment(
                    data,
                    maintype=maintype,
                    subtype=subtype,
                    filename=filename,
                )

        await self.__send_message(msg)
