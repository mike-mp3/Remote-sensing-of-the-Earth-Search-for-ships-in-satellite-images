from app.internal.repository.postgresql import PromptRepository
from app.internal.repository.repository import BaseRepository
from app.pkg.clients.rabbitmq.producer import RabbitMQProducer
from app.pkg.clients.websocket.manager import WebSocketManager
from app.pkg.logger import get_logger
from app.pkg.models import (
    ResultPromptMessage,
    UpdatePromptStatusCommand,
)
from app.pkg.models.app.prompts import PromptStatus
from app.pkg.models.exceptions.repository import EmptyResult, UniqueViolation

logger = get_logger(__name__)


class PromptService:
    prompt_repository: PromptRepository
    producer: RabbitMQProducer
    ws_manager: WebSocketManager
    raw_queue_name: str

    def __init__(
        self,
        prompt_repository: BaseRepository,
        producer: RabbitMQProducer,
        websocket_manager: WebSocketManager,
        raw_queue_name: str,
    ):
        self.prompt_repository = prompt_repository
        self.producer = producer
        self.raw_queue_name = raw_queue_name
        self.ws_manager = websocket_manager

    async def callback_handle_results(self, message: ResultPromptMessage):
        try:
            prompt = await self.prompt_repository.update_status(
                cmd=UpdatePromptStatusCommand(
                    id=message.id,
                    result_key=message.result_key,
                    status=PromptStatus.success,
                ),
            )
        except EmptyResult:
            return "empty result"

        user_id = prompt.user_id

        if self.ws_manager.is_user_connected(user_id):
            await self.ws_manager.send_personal_message(user_id, prompt)
