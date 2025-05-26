import asyncio
from collections import defaultdict
from typing import Any, Dict, Set

from app.pkg.logger import get_logger
from fastapi import WebSocket
from pydantic import PositiveInt

__all__ = ["WebSocketManager"]

from app.pkg.models.base import BaseModel

logger = get_logger(__name__)


class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[Any, Set[WebSocket]] = defaultdict(set)
        self.lock = asyncio.Lock()

    async def connect(self, user_id: PositiveInt, websocket: WebSocket):
        async with self.lock:
            await websocket.accept()
            self.active_connections[user_id].add(websocket)

    def disconnect(self, user_id: PositiveInt, websocket: WebSocket):
        self.active_connections[user_id].discard(websocket)
        if not self.active_connections[user_id]:
            del self.active_connections[user_id]

    async def send_personal_message(
        self,
        user_id: PositiveInt,
        message: BaseModel,
    ):
        async with self.lock:
            connections = self.active_connections.get(user_id, set())
            for connection in connections:
                try:
                    await connection.send_json(message.model_dump_json())
                except Exception as e:
                    logger.error(e)
                    self.disconnect(user_id, connection)

    def is_user_connected(self, user_id: PositiveInt) -> bool:
        return bool(self.active_connections.get(user_id))
