"""Models of user prompts S3 objects."""
from enum import Enum
from uuid import UUID

from app.pkg.models.base import BaseModel
from pydantic import Field

__all__ = [
    "PromptObjectType",
    "GeneratePrompt",
    "PromptLink",
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
    user_id = Field(
        description="User id",
        examples=["some-id"],
    )
    file_key = Field(
        description="Key path to object",
        examples=["raw/user_{some-id}/prompt_{some-id}"],
    )
    key_starts_with = Field(
        description="Key path to object without last postfix",
        examples=["user_{some-id}"],
    )


class PromptObjectType(str, Enum):
    RAW = "raw"
    RESULT = "results"


class BasePrompt(BaseModel):
    """Prompt base model"""


# Path Strategy
class GeneratePrompt(BasePrompt):
    object_type: PromptObjectType
    user_id: str = PromptFields.user_id
    prompt_id: str = PromptFields.prompt_id


class PromptLink(BasePrompt):
    object_type: PromptObjectType
    prompt_id: str = PromptFields.prompt_id
    user_id: str = PromptFields.user_id
    key_path: str = PromptFields.file_key
    key_starts_with: str = PromptFields.key_starts_with


# Messages - Rabbit
class RawPromptMessage(BasePrompt):
    id: UUID = PromptFields.id
    raw_key: str = PromptFields.file_key


class ResultPromptMessage(BasePrompt):
    id: UUID = PromptFields.id
    result_key: str = PromptFields.file_key
