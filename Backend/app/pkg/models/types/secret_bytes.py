"""Secret bytes types for pydantic models."""

from typing import Any
import bcrypt

__all__ = ["EncryptedSecretBytes"]

class EncryptedSecretBytes:
    """Model for verify bytes range [6;100] and crypt than by bcrypt
    algorithm."""

    min_length = 6
    max_length = 100

    def __init__(self, value: Any):
        self.value = self.validate(value)

    def __repr__(self) -> str:
        return f"EncryptedSecretBytes(b'{self.value!r}')"

    @classmethod
    def validate(cls, value: Any) -> "EncryptedSecretBytes":
        if isinstance(value, cls):
            return value
        if not isinstance(value, bytes):
            raise ValueError("Expected a bytes value")

        if len(value) < cls.min_length or len(value) > cls.max_length:
            raise ValueError(f"Length of value must be between {cls.min_length} and {cls.max_length} bytes.")

        encrypted_value = bcrypt.hashpw(value, bcrypt.gensalt())
        return cls(encrypted_value)

