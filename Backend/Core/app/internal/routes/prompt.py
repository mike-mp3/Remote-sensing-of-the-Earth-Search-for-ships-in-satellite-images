from typing import List

from app.internal.pkg.handlers import with_errors
from app.internal.services import Services
from app.internal.services.prompt import PromptService
from app.pkg.models import (
    ActiveUser,
    ConfirmPromptRequest,
    PaginationQuery,
    PresidnedGetResponse,
    PresignedGetRequest,
    PresignedPostRequest,
    PresignedPostResponse,
    Prompt,
    PromptPageRequest,
)
from app.pkg.models.exceptions import (
    CannotProcessPrompt,
    InvalidPromptPath,
    PromptNotFound,
    RawPromptAlreadyExists,
    RawPromptNowFound,
)
from app.pkg.utils.jwt import get_current_user
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query, status

router = APIRouter(prefix="/prompt", tags=["Prompt"])


@router.post(
    "/generate-s3-presigned-post",
    status_code=status.HTTP_200_OK,
    response_model=PresignedPostResponse,
    description="Generate presigned post url and data to upload to S3",
)
@inject
async def generate_s3_presigned_post(
    prompt_service: PromptService = Depends(Provide[Services.prompt_service]),
    user: ActiveUser = Depends(get_current_user),
):
    return await prompt_service.generate_presigned_post(
        request=PresignedPostRequest(
            user_id=user.id,
        ),
    )


@router.post(
    "/confirm",
    status_code=status.HTTP_201_CREATED,
    response_model=Prompt,
    description="Start to process the prompt",
)
@with_errors(
    InvalidPromptPath,
    RawPromptNowFound,
    RawPromptAlreadyExists,
    CannotProcessPrompt,
)
@inject
async def confirm(
    req: ConfirmPromptRequest,
    prompt_service: PromptService = Depends(Provide[Services.prompt_service]),
    user: ActiveUser = Depends(get_current_user),
):
    return await prompt_service.confirm_prompt(
        request=req,
        active_user=user,
    )


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=List[Prompt],
    description="Get prompts with pagination",
)
@with_errors(PromptNotFound)
@inject
async def get_prompt_page(
    query: PaginationQuery = Query(),
    prompt_service: PromptService = Depends(Provide[Services.prompt_service]),
    user: ActiveUser = Depends(get_current_user),
):
    return await prompt_service.get_page(
        request=PromptPageRequest(
            **query.model_dump(),
        ),
        active_user=user,
    )


@router.post(
    "/generate-s3-presigned-get",
    status_code=status.HTTP_200_OK,
    response_model=List[PresidnedGetResponse],
    description="Generate presigned get url for downloading image(s)",
)
@inject
async def generate_s3_presigned_get(
    req: PresignedGetRequest,
    prompt_service: PromptService = Depends(Provide[Services.prompt_service]),
    user: ActiveUser = Depends(get_current_user),
):
    return await prompt_service.generate_presigned_get(
        request=req,
        active_user=user,
    )


@router.post(
    "/test_send_to_rabbit",
)
@inject
async def test(
    prompt_service: PromptService = Depends(Provide[Services.prompt_service]),
):
    return await prompt_service.test()
