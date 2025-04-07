"""Models of user prompts S3 objects."""
from enum import Enum
from typing import Any

from pydantic import Field, PositiveInt

from app.pkg.models.app.user import UserFields
from app.pkg.models.base import BaseModel

__all__ = [
    "PromptObjectType",
    "GeneratePromptLink",
    "PromptLink",
    "PrompterClientResponse",
]


class PromptLinkFields:
    prompt_id = Field(
        description="Prompt id",
        examples=["some-id"],
    )
    user_id = UserFields.id
    key_path = Field(
        description="Key path to object",
        examples=["user_{some-id}/prompt_{some-id}"],
    )
    key_starts_with = Field(
        description="Key path to object without last postfix",
        examples=["user_{some-id}"],
    )


class BasePromptLink(BaseModel):
    """Prompt base model"""


# Path Strategy
class PromptObjectType(str, Enum):
    RAW = "raw"
    RESULT = "results"

class GeneratePromptLink(BasePromptLink):
    object_type: PromptObjectType
    user_id: PositiveInt = PromptLinkFields.user_id
    prompt_id: str = PromptLinkFields.prompt_id

class PromptLink(BasePromptLink):
    object_type: PromptObjectType
    prompt_id: str = PromptLinkFields.prompt_id
    user_id: PositiveInt = PromptLinkFields.user_id
    key_path: str = PromptLinkFields.key_path
    key_starts_with: str = PromptLinkFields.key_starts_with


# Client
class PrompterClientResponse(BasePromptLink):
    s3_response: Any
    link: PromptLink