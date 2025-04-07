from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import Provide, inject

from app.internal.pkg.handlers import with_errors
from app.internal.services import Services
from app.internal.services.prompt import PromptService
from app.pkg.models import (
    ActiveUser,
    PresignedPostRequest,
    ConfirmPromptRequest,
    PresignedPostResponse,
    Prompt
)
from app.pkg.models.exceptions import InvalidPromptPath, RawPromptNowFound, RawPromptAlreadyExists
from app.pkg.utils.jwt import get_current_user

router = APIRouter(prefix="/prompt", tags=["Prompt"])


@router.post(
    "/generate-s3-presigned-post",
    status_code=status.HTTP_201_CREATED,
    response_model=PresignedPostResponse,
    description="Generate presigned post url and data to upload to S3",
)
@inject
async def generate_s3_presigned_post(
    prompt_service: PromptService = Depends(Provide[Services.prompt_service]),
    user: ActiveUser = Depends(get_current_user)
):
    return await prompt_service.generate_presigned_post(
        request=PresignedPostRequest(
            user_id=user.id,
        )
    )


@router.post(
    "/confirm",
    status_code=status.HTTP_201_CREATED,
    response_model=Prompt,
    description="Start to process the prompt"
)
@with_errors(
    InvalidPromptPath,
    RawPromptNowFound,
    RawPromptAlreadyExists
)
@inject
async def confirm(
    req: ConfirmPromptRequest,
    prompt_service: PromptService = Depends(Provide[Services.prompt_service]),
    user: ActiveUser = Depends(get_current_user)
):
    return await prompt_service.confirm_prompt(
        request=req, active_user=user,
    )

