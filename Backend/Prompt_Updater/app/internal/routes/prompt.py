from app.internal.services import Services
from app.pkg.clients.websocket.manager import WebSocketManager
from app.pkg.models import (
    ActiveUser,
)
from app.pkg.utils.jwt import get_current_user_websocket
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

router = APIRouter(prefix="/prompt", tags=["Prompt"])


@router.websocket("/result")
@inject
async def refresh_prompt_status(
    websocket: WebSocket,
    user: ActiveUser = Depends(get_current_user_websocket),
    ws_manager: WebSocketManager = Depends(Provide[Services.clients.websocket.manager]),
):
    await ws_manager.connect(user.id, websocket)
    try:
        while True:
            pass
    except WebSocketDisconnect:
        ws_manager.disconnect(user.id, websocket)
