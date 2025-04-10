"""Models of user prompts S3 objects."""
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from app.pkg.models.app.user import UserFields
from app.pkg.models.base import BaseModel
from pydantic import AnyUrl, Field, PositiveInt

__all__ = [
    "PromptObjectType",
    "GeneratePrompt",
    "Prompt",
    "CreatePromptCommand",
    "ValidatePromptPath",
    "PresignedPostRequest",
    "ConfirmPromptRequest",
    "PromptLink",
    "PresignedPostResponse",
    "PutPromptMessage",
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
    key_path = Field(
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


class PromptObjectType(str, Enum):
    RAW = "raw"
    RESULT = "results"


class PromptStatus(str, Enum):
    pending = "pending"
    success = "success"
    error = "error"
    cancelled = "cancelled"


class BasePrompt(BaseModel):
    """Prompt base model"""


# Representation layer
class PresignedPostRequest(BasePrompt):
    user_id: PositiveInt = PromptFields.user_id


class PresignedPostFields(BaseModel):
    content_type: str = Field(
        examples=["image/"],
        alias="Content-Type",
    )
    key: str = PromptFields.key_path
    aws_access_key_id: str = Field(
        examples=["user"],
        alias="AWSAccessKeyId",
    )
    policy: str = Field(
        examples=["policy"],
    )
    signature: str = Field(
        examples=["signature"],
    )


class PresignedPostResponse(BaseModel):
    url: AnyUrl = Field(examples=["http://example.com"])
    fields: PresignedPostFields


class ConfirmPromptRequest(BasePrompt):
    key_path: str = PromptFields.key_path


# Path Strategy
class GeneratePrompt(BasePrompt):
    object_type: PromptObjectType
    user_id: PositiveInt = PromptFields.user_id
    prompt_id: str = PromptFields.prompt_id


class PromptLink(BasePrompt):
    object_type: PromptObjectType
    prompt_id: str = PromptFields.prompt_id
    user_id: PositiveInt = PromptFields.user_id
    key_path: str = PromptFields.key_path
    key_starts_with: str = PromptFields.key_starts_with


class ValidatePromptPath(BasePrompt):
    path: str
    user_id: Optional[int] = None
    object_type: Optional[str] = None
    prompt_id: Optional[str] = None


# Commands - SQL
class CreatePromptCommand(BasePrompt):
    user_id: PositiveInt = PromptFields.user_id
    prompt_id: str = PromptFields.prompt_id
    raw_key: str = PromptFields.key_path


class Prompt(BasePrompt):
    id: UUID = PromptFields.id
    user_id: PositiveInt = PromptFields.user_id
    prompt_id: str = PromptFields.prompt_id
    raw_key: str = PromptFields.key_path
    result_key: Optional[str] = PromptFields.key_path
    status: PromptStatus = PromptFields.status
    created_at: datetime = PromptFields.created_at
    updated_at: datetime = PromptFields.updated_at


# Messages - Rabbit
class PutPromptMessage(BasePrompt):
    id: UUID = PromptFields.id
    raw_key: str = PromptFields.key_path
