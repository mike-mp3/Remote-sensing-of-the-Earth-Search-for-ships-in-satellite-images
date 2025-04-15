"""Models of user prompts S3 objects."""
from uuid import UUID

from app.pkg.models.app.user import UserFields
from app.pkg.models.base import BaseModel
from pydantic import Field

__all__ = [
    "PromptFields",
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


# Messages - Rabbit
class RawPromptMessage(BasePrompt):
    id: UUID = PromptFields.id
    raw_key: str = PromptFields.file_key


class ResultPromptMessage(BasePrompt):
    id: UUID = PromptFields.id
    result_key: str = PromptFields.file_key
