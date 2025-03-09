"""Strings types for pydantic models."""

from __future__ import annotations
from pydantic import SecretStr, model_validator

__all__ = ["NotEmptySecretStr", "NotEmptyStr"]


# TODO: Use generic pydantic model for create min and max range
class NotEmptySecretStr(SecretStr):
    """Validate, that length of the string is greater than or equal to 1."""

    min_length = 1

    @classmethod
    def __repr__(cls) -> str:
        # Для отображения значения SecretStr без раскрытия секрета
        return f"NotEmptySecretStr('{cls.get_secret_value()}')"

    @model_validator(mode="before")
    def validate_not_empty(cls, value: str) -> str:
        """Check that the string has a valid length."""
        if len(value) < cls.min_length:
            raise ValueError(f"String length must be at least {cls.min_length} characters")
        return value


class NotEmptyStr(str):
    """Validate, that length of string is greater than 0."""

    min_length: int | None = 1
    max_length: int | None = None

    @classmethod
    def __modify_schema__(cls, field_schema: dict[str, str]) -> None:
        """Modify the OpenAPI schema for this type."""
        field_schema.update(
            {
                "type": "string",
                "minLength": cls.min_length,
                "maxLength": cls.max_length,
                "writeOnly": False,  # you can change this as needed
            }
        )

    @classmethod
    def __get_validators__(cls):
        """Override the validators for this type."""
        yield cls.validate_length

    @classmethod
    def validate_length(cls, value: str) -> str:
        """Ensure the length of the string is within bounds."""
        if len(value) < cls.min_length:
            raise ValueError(f"Length must be greater than or equal to {cls.min_length}")
        if cls.max_length and len(value) > cls.max_length:
            raise ValueError(f"Length must be less than or equal to {cls.max_length}")
        return value

    def __repr__(self) -> str:
        return f"NotEmptyStr('{self}')"
