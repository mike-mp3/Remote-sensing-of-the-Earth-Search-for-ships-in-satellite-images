from fastapi import APIRouter, Depends, status

from app.pkg import models

from dependency_injector.wiring import Provide, inject
from app.internal.services import Services
from app.internal.services.user import UserService
import psycopg2

router = APIRouter(prefix="/user", tags=["user"])



@router.post(
    "",
    response_model=models.CreateUserResponse,
    status_code=status.HTTP_201_CREATED,
    description="Create user",
)
@inject
async def create_user(
    cmd: models.CreateUserRequest,
    user_service: UserService = Depends(Provide[Services.user_service])
):
    return await user_service.create_user(cmd)


# не используемая ручка. просто потыкать для теста
@router.post(
    "/send-email"
)
@inject
async def create_user(
    user_service: UserService = Depends(Provide[Services.user_service])
):
    return await user_service.useless_mock()