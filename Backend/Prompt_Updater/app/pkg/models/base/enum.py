"""All enum inside models must be inherited by :class:`.BaseEnum`"""

from enum import Enum

__all__ = ["BaseEnum"]


class BaseEnum(str, Enum):
    """Base ENUM model."""
