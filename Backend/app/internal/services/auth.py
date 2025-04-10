from app.internal.repository.postgresql import JWTRefreshTokenRepository, UserRepository
from app.internal.repository.repository import BaseRepository
from app.pkg.logger import get_logger
from app.pkg.models import (
    AuthRequest,
    CreateJWTRefreshTokenCommand,
    CreateOrUpdateJWTRefreshTokenCommand,
    DeleteJWTRefreshTokenCommand,
    JWTRefreshToken,
    ReadJWTRefreshTokenQuery,
    ReadUserByEmailCommand,
    UpdateJWTRefreshTokenCommand,
    User,
)
from app.pkg.models.exceptions.auth import IncorrectUsernameOrPassword
from app.pkg.models.exceptions.jwt import UnAuthorized
from app.pkg.models.exceptions.repository import EmptyResult
from app.pkg.utils.password import verify_password

logger = get_logger(__name__)


class AuthService:
    """Service authorization and authentication user management."""

    refresh_token_repository: JWTRefreshTokenRepository
    user_repository: UserRepository

    def __init__(
        self,
        refresh_token_repository: BaseRepository,
        user_repository: BaseRepository,
    ):
        self.refresh_token_repository = refresh_token_repository
        self.user_repository = user_repository

    async def check_password(self, request: AuthRequest) -> User:
        try:
            user = await self.user_repository.read_by_email(
                cmd=ReadUserByEmailCommand(
                    email=request.email,
                ),
            )
        except EmptyResult:
            raise IncorrectUsernameOrPassword

        if not verify_password(request.password, user.password):
            raise IncorrectUsernameOrPassword

        return user

    async def update_or_create_refresh_token(
        self,
        request: CreateOrUpdateJWTRefreshTokenCommand,
    ) -> JWTRefreshToken:
        try:
            return await self.refresh_token_repository.update(
                cmd=UpdateJWTRefreshTokenCommand(
                    user_id=request.user_id,
                    refresh_token=request.refresh_token,
                ),
            )
        except EmptyResult:
            return await self.refresh_token_repository.create(
                cmd=CreateJWTRefreshTokenCommand(
                    user_id=request.user_id,
                    refresh_token=request.refresh_token,
                ),
            )

    async def check_refresh_token_exists(
        self,
        request: ReadJWTRefreshTokenQuery,
    ) -> JWTRefreshToken:
        try:
            return await self.refresh_token_repository.read(
                query=request,
            )
        except EmptyResult:
            raise UnAuthorized

    async def delete_refresh_token(
        self,
        request: DeleteJWTRefreshTokenCommand,
    ) -> JWTRefreshToken:
        try:
            return await self.refresh_token_repository.delete(
                cmd=request,
            )
        except EmptyResult:
            raise UnAuthorized
