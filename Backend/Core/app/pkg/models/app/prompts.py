"""Models of user prompts S3 objects."""
from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import UUID

from app.pkg.models.app.user import UserFields
from app.pkg.models.base import BaseModel
from pydantic import AnyUrl, Field, PositiveInt, model_validator

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
    "RawPromptMessage",
    "ResultPromptMessage",
    "UpdatePromptStatusCommand",
    "PaginationQuery",
    "PromptPageRequest",
    "ReadPromptCommand",
    "ReadPromptPageCommand",
    "PromptPageRequest",
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
    page_size = Field(
        description="Prompt page size",
        examples=["30"],
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
    key: str = PromptFields.file_key
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
    key_path: str = PromptFields.file_key


class PaginationQuery(BaseModel):
    size: PositiveInt = Field(
        default=30,
        le=100,
        description="Prompts quantity, no more than 100",
    )
    created_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp-ISO cursor for the next page",
    )
    prompt_id: Optional[UUID] = Field(
        default=None,
        description="Prompt uuid",
    )

    @model_validator(mode="after")
    def check_cursor_options(self):
        are_received = (
            bool(self.created_at),
            bool(self.prompt_id),
        )
        if any(are_received) and not all(are_received):
            raise ValueError("All cursor options must be given")
        return self


# Service external requests
class PromptPageRequest(BasePrompt):
    size: PositiveInt
    created_at: Optional[datetime] = None
    prompt_id: Optional[UUID] = None


# Path Strategy
class GeneratePrompt(BasePrompt):
    object_type: PromptObjectType
    user_id: PositiveInt = PromptFields.user_id
    prompt_id: str = PromptFields.prompt_id


class PromptLink(BasePrompt):
    object_type: PromptObjectType
    prompt_id: str = PromptFields.prompt_id
    user_id: PositiveInt = PromptFields.user_id
    key_path: str = PromptFields.file_key
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
    raw_key: str = PromptFields.file_key


class UpdatePromptStatusCommand(BasePrompt):
    id: UUID = PromptFields.id
    result_key: str = PromptFields.file_key
    status: PromptStatus = PromptFields.status


class ReadPromptCommand(BasePrompt):
    user_id: PositiveInt = PromptFields.user_id
    size: PositiveInt = PromptFields.page_size


class ReadPromptPageCommand(BasePrompt):
    user_id: PositiveInt = PromptFields.user_id
    size: PositiveInt = PromptFields.page_size
    prompt_id: UUID = PromptFields.id
    created_at: datetime = PromptFields.created_at


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
