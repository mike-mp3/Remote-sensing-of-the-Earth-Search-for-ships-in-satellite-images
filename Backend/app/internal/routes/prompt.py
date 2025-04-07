from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import Provide, inject

from app.internal.services import Services
from app.internal.services.prompt import PromptService

router = APIRouter(prefix="/prompt", tags=["Prompt"])


@router.post(
    "/test_s3_client",
    status_code=status.HTTP_200_OK,
)
@inject
async def test_get_presigned_post(
    prompt_service: PromptService = Depends(Provide[Services.prompt_service])
):
    return await prompt_service.get_presigned_post()
