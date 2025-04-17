"""LoggerLevel model."""
from enum import Enum

__all__ = ["LoggerLevel"]


class LoggerLevel(str, Enum):
    WARNING = "WARNING"
    INFO = "INFO"
    ERROR = "ERROR"
    DEBUG = "DEBUG"
    CRITICAL = "CRITICAL"
    NOTSET = "NOTSET"
