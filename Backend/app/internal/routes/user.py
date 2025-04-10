from app.internal.pkg.handlers import with_errors
from app.internal.services import Services
from app.internal.services.user import UserService
from app.pkg import models
from app.pkg.models import exceptions as excs
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

router = APIRouter(prefix="/user", tags=["User"])


@router.post(
    "",
    response_model=models.CreateUserResponse,
    status_code=status.HTTP_201_CREATED,
    description="Create user",
)
@with_errors(excs.UserAlreadyExists)
@inject
async def create_user(
    req: models.CreateUserRequest,
    user_service: UserService = Depends(Provide[Services.user_service]),
):
    return await user_service.create_user(req)


@router.post(
    "/confirm",
    status_code=status.HTTP_200_OK,
    description="Confirm user email after registration with code",
)
@with_errors(excs.CodeNotFound, excs.IncorrectCode)
@inject
async def confirm_user_email(
    req: models.ConfirmUserEmailRequest,
    user_service: UserService = Depends(Provide[Services.user_service]),
):
    return await user_service.confirm_email(req)


@router.post(
    "/confirm/resend-email",
    status_code=status.HTTP_200_OK,
    description="Resend confirmation code to user email",
)
@inject
async def resend_user_email(
    req: models.ResendUserConfirmationCodeRequest,
    user_service: UserService = Depends(Provide[Services.user_service]),
):
    return await user_service.resend_confirmation_code(req)
