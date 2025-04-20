from app.pkg.clients import Clients
from app.pkg.clients.email_client import EmailClient
from app.pkg.logger import get_logger
from app.pkg.tasks.celery.celery_app import celery_app
from app.pkg.tasks.celery.decorators import async_to_sync
from dependency_injector.wiring import Provide, inject
from pydantic import EmailStr

logger = get_logger(__name__)


class EmailTasks:
    @staticmethod
    @celery_app.task(name="send_confirmation_code", bind=True, max_retries=3)
    @inject
    @async_to_sync
    async def send_confirmation_code(
        task,
        to_email: EmailStr,
        confirmation_code: str,
        email_client: EmailClient = Provide[Clients.email.client],
    ):
        try:
            await email_client.send_confirmation(
                to_email=to_email,
                confirmation_code=confirmation_code,
            )
        except Exception as exc:
            if task.request.retries >= task.max_retries:
                logger.info(
                    "Sending email with confirmation code to %s failed: %s",
                    to_email,
                    exc,
                )
            else:
                logger.error(
                    "Resending email with confirmation code to %s failed: %s",
                    to_email,
                    exc,
                )
                task.retry(countdown=30, exc=exc)
