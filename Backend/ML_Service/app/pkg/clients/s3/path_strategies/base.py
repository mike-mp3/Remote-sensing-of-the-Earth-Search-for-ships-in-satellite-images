from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from app.pkg.models.base import BaseModel

BasePathStrategy = TypeVar("BasePathStrategy", bound="PathStrategy")
Command = TypeVar("Command", bound=BaseModel)
Output = TypeVar("Output", bound=BaseModel)


class PathStrategy(ABC, Generic[Command, Output]):
    @property
    @abstractmethod
    def _template(self) -> str:
        pass

    @property
    @abstractmethod
    def _pattern(self) -> str:
        pass

    @classmethod
    def generate_path(cls, cmd: Command) -> Output:
        pass

    @classmethod
    def parse(cls, path: str) -> Output:
        pass
