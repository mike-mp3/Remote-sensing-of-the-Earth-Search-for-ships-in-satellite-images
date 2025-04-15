"""Models of user prompts S3 objects."""
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from app.pkg.models.app.user import UserFields
from app.pkg.models.base import BaseModel
from pydantic import Field, PositiveInt

__all__ = [
    "PromptFields",
    "PromptStatus",
    "Prompt",
    "RawPromptMessage",
    "ResultPromptMessage",
]


class PromptFields:
    id = Field(
        description="Unique user prompt id in database",
        examples=["some-id"],
    )
    prompt_id = Field(
        description="Prompt id",
        examples=["some-id"],
    )
    user_id = UserFields.id
    file_key = Field(
        description="Key path to object",
        examples=["raw/user_{some-id}/prompt_{some-id}"],
    )
    key_starts_with = Field(
        description="Key path to object without last postfix",
        examples=["user_{some-id}"],
    )
    status = Field(
        description="Prompt status",
        examples=["pending", "success", "error", "cancelled"],
    )
    created_at = Field(
        description="Prompt creation time",
        examples=[""],
    )
    updated_at = Field(
        description="Prompt status update time",
        examples=[""],
    )


class BasePrompt(BaseModel):
    """Prompt base model"""


class PromptStatus(str, Enum):
    pending = "pending"
    success = "success"
    error = "error"
    cancelled = "cancelled"


class Prompt(BasePrompt):
    id: UUID = PromptFields.id
    user_id: PositiveInt = PromptFields.user_id
    prompt_id: str = PromptFields.prompt_id
    raw_key: str = PromptFields.file_key
    result_key: Optional[str] = PromptFields.file_key
    status: PromptStatus = PromptFields.status
    created_at: datetime = PromptFields.created_at
    updated_at: datetime = PromptFields.updated_at


# Messages - Rabbit
class RawPromptMessage(BasePrompt):
    id: UUID = PromptFields.id
    raw_key: str = PromptFields.file_key


class ResultPromptMessage(BasePrompt):
    id: UUID = PromptFields.id
    result_key: str = PromptFields.file_key
