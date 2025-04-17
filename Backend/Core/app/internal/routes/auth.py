from app.internal.pkg.handlers import with_errors
from app.internal.services import AuthService, Services
from app.pkg.models import (
    ActiveUser,
    CreateOrUpdateJWTRefreshTokenCommand,
    CreateUserRequest,
    DeleteJWTRefreshTokenCommand,
    ReadJWTRefreshTokenQuery,
    UserRoleEnum,
)
from app.pkg.models.exceptions import (
    IncorrectUsernameOrPassword,
    TokenTimeExpired,
    UnAuthorized,
    UserIsNotActivated,
    WrongToken,
)
from app.pkg.utils.jwt import (
    JWT,
    JwtAccessCookie,
    JwtAuthorizationCredentials,
    JwtRefreshCookie,
    get_current_user,
    refresh_security,
)
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response, Security, status
from pydantic import SecretStr

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    description="Authenticate user",
)
@with_errors(
    UserIsNotActivated,
    IncorrectUsernameOrPassword,
)
@inject
async def auth_user(
    response: Response,
    req: CreateUserRequest,
    access_util: JwtAccessCookie = Depends(Provide[JWT.access]),
    refresh_util: JwtRefreshCookie = Depends(Provide[JWT.refresh]),
    auth_service: AuthService = Depends(Provide[Services.auth_service]),
) -> None:
    user = await auth_service.check_password(request=req)
    if not user.is_activated:
        raise UserIsNotActivated

    access_token = access_util.create_access_token(
        subject={
            "user_id": user.id,
            "email": user.email,
            "role_name": UserRoleEnum(user.role_id).name,
            "is_activated": user.is_activated,
        },
    )
    refresh_token = refresh_util.create_refresh_token(
        subject={
            "user_id": user.id,
            "email": user.email,
            "role_name": UserRoleEnum(user.role_id).name,
            "is_activated": user.is_activated,
        },
    )

    # С логикой try/except внутри
    await auth_service.update_or_create_refresh_token(
        request=CreateOrUpdateJWTRefreshTokenCommand(
            refresh_token=SecretStr(refresh_token),
            user_id=user.id,
        ),
    )
    access_util.set_account_cookie(response=response, access_token=access_token)
    refresh_util.set_refresh_cookie(response=response, refresh_token=refresh_token)


# todo: подумать над тем, чтобы refresh обновлялся в БД
# todo: а не приходилось перелогиниваться раз в ... дней
@router.patch(
    "/refresh",
    description="Get new access token",
)
@with_errors(UnAuthorized)
@inject
async def create_new_token_pair(
    response: Response,
    access_util: JwtAccessCookie = Depends(Provide[JWT.access]),
    refresh_util: JwtRefreshCookie = Depends(Provide[JWT.refresh]),
    credentials: JwtAuthorizationCredentials = Security(refresh_security),
    auth_service: AuthService = Depends(Provide[Services.auth_service]),
):

    user_id = credentials.subject.get("user_id")
    role_name = credentials.subject.get("role_name")
    email = credentials.subject.get("email")
    is_activated = credentials.subject.get("is_activated")
    # ↑ если нет Cookie, внутри произойдет raise UnAuthorized

    if not all((user_id, role_name, email, is_activated)):
        raise UnAuthorized

    refresh_token = await auth_service.check_refresh_token_exists(
        request=ReadJWTRefreshTokenQuery(
            user_id=user_id,
            refresh_token=credentials.raw_token,
        ),
    )

    access_token = access_util.create_access_token(
        subject={
            "user_id": user_id,
            "email": email,
            "role_name": role_name,
            "is_activated": is_activated,
        },
    )
    access_util.set_account_cookie(response=response, access_token=access_token)
    refresh_util.set_refresh_cookie(response=response, refresh_token=refresh_token)


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    description="Logout user",
)
@with_errors(UnAuthorized)
@inject
async def logout(
    auth_service: AuthService = Depends(Provide[Services.auth_service]),
    credentials: JwtAuthorizationCredentials = Security(refresh_security),
) -> None:
    user_id = credentials.subject.get("user_id")
    refresh_token = credentials.raw_token
    # ↑ если нет Cookie, внутри произойдет raise UnAuthorized

    if not (user_id and refresh_token):
        raise UnAuthorized

    await auth_service.delete_refresh_token(
        request=DeleteJWTRefreshTokenCommand(
            user_id=user_id,
            refresh_token=refresh_token,
        ),
    )


@router.get(
    "/test",
    status_code=status.HTTP_200_OK,
    description="test",
)
@inject
@with_errors(
    UnAuthorized,
    TokenTimeExpired,
    WrongToken,
)
async def test(
    user: ActiveUser = Depends(get_current_user),
):
    return user
