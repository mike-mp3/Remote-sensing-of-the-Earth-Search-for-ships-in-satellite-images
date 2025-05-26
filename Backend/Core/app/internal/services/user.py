from app.internal.repository.async_redis import UserAsyncRedisRepository
from app.internal.repository.postgresql import UserRepository
from app.internal.repository.repository import BaseRepository
from app.pkg import models
from app.pkg.logger import get_logger
from app.pkg.models.exceptions import UserAlreadyExists
from app.pkg.models.exceptions.repository import EmptyResult
from app.pkg.models.exceptions.user import CodeNotFound, IncorrectCode, UserNotFound
from app.pkg.tasks.celery.email import EmailTasks
from app.pkg.utils.confirmation_code import generate_secure_code, verify_secure_code
from app.pkg.utils.password import hash_password
from pydantic import EmailStr, SecretBytes, SecretStr

logger = get_logger(__name__)


class UserService:
    """Service for manage users."""

    user_repository: UserRepository
    user_redis_repository: UserAsyncRedisRepository
    email_tasks: EmailTasks

    def __init__(
        self,
        user_repository: BaseRepository,
        user_redis_repository: BaseRepository,
        email_tasks: EmailTasks,
    ):
        self.user_repository = user_repository
        self.user_redis_repository = user_redis_repository
        self.email_tasks = email_tasks

    async def create_user(self, request: models.CreateUserRequest):
        user = None
        encrypted_password: SecretBytes = hash_password(request.password)
        try:
            user = await self.user_repository.upsert_inactive_user(
                cmd=models.CreateUserCommand(
                    email=request.email,
                    password=encrypted_password,
                ),
            )
        except EmptyResult:
            raise UserAlreadyExists
        except Exception as err:
            logger.error("Failed to create user id database: %s", err)

        try:
            await self.__send_confirmation_code(request.email)
        except Exception as err:
            logger.error("Failed to send confirmation code: %s", err)

        return user

    async def confirm_email(
        self,
        request: models.ConfirmUserEmailRequest,
    ) -> None:
        real_code: SecretStr = await self.user_redis_repository.read(
            cmd=models.ReadUserConfirmationCode(
                email=request.email,
            ),
        )
        if not real_code.get_secret_value():
            raise CodeNotFound
        if not verify_secure_code(request.confirmation_code, real_code):
            raise IncorrectCode
        try:
            await self.user_repository.update_user_status(
                cmd=models.UpdateUserStatusCommand(
                    email=request.email,
                    is_activated=True,
                ),
            )
        except EmptyResult:
            logger.warning("After user creation there is no user in database")
            raise UserNotFound

    # не надо в бд проверять
    async def resend_confirmation_code(
        self,
        request: models.ResendUserConfirmationCodeRequest,
    ) -> None:
        try:
            await self.__send_confirmation_code(request.email)
        except Exception as err:
            logger.error("Failed to create user: %s", err)

    async def __send_confirmation_code(
        self,
        email: EmailStr,
    ):
        confirmation_code: SecretStr = generate_secure_code(digits=6)
        await self.user_redis_repository.create(
            cmd=models.CreateUserConfirmationCode(
                email=email,
                confirmation_code=confirmation_code,
            ),
        )
        self.email_tasks.send_confirmation_code.delay(
            to_email=email,
            confirmation_code=confirmation_code.get_secret_value(),
        )
        logger.debug(
            "Added email confirmation background task for user %s",
            email,
        )
