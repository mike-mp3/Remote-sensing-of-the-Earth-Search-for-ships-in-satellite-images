import psycopg2

from app.internal.repository.postgresql import user
from app.internal.repository.repository import BaseRepository
from app.pkg import models
from app.pkg.clients.email_client.base.template import BaseEmailTemplate
from app.pkg.logger import get_logger
from app.pkg.models.exceptions import UserAlreadyExists
from app.pkg.utils.password import hash_password

from pydantic import SecretBytes


logger = get_logger(__name__)

class UserService:
    """Service for manage users."""

    user_repository: user.UserRepository
    email_clients: BaseEmailTemplate


    def __init__(
        self,
        user_repository: BaseRepository,
        email_confirmation: BaseEmailTemplate
    ):
        self.user_repository = user_repository
        self.email_confirmation = email_confirmation

    async def create_user(self, request: models.CreateUserRequest):
        encrypted_password: SecretBytes = hash_password(request.password)

        try:
            return await self.user_repository.create(
                cmd=models.CreateUserCommand(
                    email=request.email,
                    password=encrypted_password,
                )
            )
        except psycopg2.errors.UniqueViolation:
            raise UserAlreadyExists


    async def useless_mock(self):
        await self.email_confirmation.send("example@mail.ru", "111")
