from app.internal.pkg.handlers import with_errors
from app.internal.services import Services
from app.internal.services.prompt import PromptService
from app.pkg.clients import Clients
from app.pkg.clients.websocket.manager import WebSocketManager
from app.pkg.models import (
    ActiveUser,
    ConfirmPromptRequest,
    PresignedPostRequest,
    PresignedPostResponse,
    Prompt,
)
from app.pkg.models.exceptions import (
    CannotProcessPrompt,
    InvalidPromptPath,
    RawPromptAlreadyExists,
    RawPromptNowFound,
)
from app.pkg.utils.jwt import get_current_user, get_current_user_websocket
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, status

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


@router.websocket("/result")
@inject
async def refresh_prompt_status(
    websocket: WebSocket,
    user: ActiveUser = Depends(get_current_user_websocket),
    ws_manager: WebSocketManager = Depends(Provide[Clients.websocket.manager]),
):
    await ws_manager.connect(user.id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await ws_manager.send_personal_message(user.id, f"You said: {data}")
    except WebSocketDisconnect:
        ws_manager.disconnect(user.id, websocket)


@router.post(
    "/test",
)
@inject
async def test(
    prompt_service: PromptService = Depends(Provide[Services.prompt_service]),
):
    return await prompt_service.test()
