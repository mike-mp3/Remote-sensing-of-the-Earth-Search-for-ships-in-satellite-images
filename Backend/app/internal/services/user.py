import psycopg2
from pydantic import SecretBytes, SecretStr

from app.internal.repository.postgresql import (
    UserRepository,
)
from app.internal.repository.repository import BaseRepository
from app.internal.workers.background import background_worker
from app.pkg import models
from app.pkg.clients.email_client.base.template import BaseEmailTemplate
from app.pkg.logger import get_logger
from app.pkg.models.exceptions import UserAlreadyExists
from app.pkg.utils.confirmation_code import generate_secure_code
from app.pkg.utils.password import hash_password


logger = get_logger(__name__)

class UserService:
    """Service for manage users."""

    user_repository: UserRepository
    email_confirmation: BaseEmailTemplate
    redis: BaseRepository

    def __init__(
        self,
        user_repository: BaseRepository,
        redis: BaseRepository,
        email_confirmation: BaseEmailTemplate,
    ):
        self.user_repository = user_repository
        self.email_confirmation = email_confirmation
        self.redis = redis

    async def create_user(self, request: models.CreateUserRequest):
        encrypted_password: SecretBytes = hash_password(request.password)
        try:
            user = await self.user_repository.create(
                cmd=models.CreateUserCommand(
                    email=request.email,
                    password=encrypted_password,
                )
            )
        except psycopg2.errors.UniqueViolation:
            raise UserAlreadyExists

        try:
            confirmation_code: SecretStr = generate_secure_code(digits=6)
            self.redis.create(
                models.CreateUserConfirmationCode(
                    email=user.email,
                    confirmation_code=confirmation_code,
                )
            )
            await background_worker.put(
                self.email_confirmation.send,
                user.email,
                confirmation_code,
            )

            logger.debug(
                "Added email confirmation background "
                "task for user %s", user.email
            )
            print(user)
            return user
        except Exception as err:
            logger.error("Failed to create user: %s", err)


    async def useless_mock(self):
        logger.debug("Adding email task to background worker")
        await background_worker.put(
            self.email_confirmation.send,
            "agl-100@mail.ru",
            SecretStr("111"),
         )
