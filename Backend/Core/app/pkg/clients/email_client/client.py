from datetime import UTC, datetime

from app.pkg.clients.email_client.base.dispatcher import BaseEmailDispatcher
from pydantic import EmailStr, SecretStr


class EmailClient:
    def __init__(self, dispatcher: BaseEmailDispatcher):
        self.dispatcher = dispatcher

    async def send_confirmation(self, to_email: EmailStr, confirmation_code: str):
        subject = "Email Confirmation"
        body = (
            f"Your confirmation code: {confirmation_code}\n\n"
            f"Enter it in the application to complete the registration."
        )
        await self.dispatcher.send(to_email, subject, body)

    async def send_report_about_prompts(
        self,
        to_email: EmailStr,
        file: bytes,
    ):
        subject = "Your PDF report"
        body = "The attachment contains your report in PDF format."
        now_str = datetime.now(UTC).strftime("%Y-%m-%d_%H-%M")
        filename = f"Orion_{now_str}.pdf"

        await self.dispatcher.send(
            to_email=to_email,
            subject=subject,
            body=body,
            attachments=[
                (file, "application/pdf", filename),
            ],
        )
