import re
from typing import Optional
from pydantic_core._pydantic_core import ValidationError

from app.pkg.models import GeneratePrompt, PromptLink
from .base import PathStrategy


class PrompterPathStrategy(PathStrategy[GeneratePrompt, PromptLink]):
    _template: str = "{object_type}/user_{user_id}/prompt_{prompt_id}"
    _pattern = re.compile(
        r"^(?P<object_type>[^/]+)/user_(?P<user_id>[^/]+)/prompt_(?P<prompt_id>[^/]+)/?$"
    )

    @classmethod
    def generate_path(cls, cmd: GeneratePrompt) -> PromptLink:
        key_path = cls._template.format(
            object_type=cmd.object_type,
            user_id=cmd.user_id,
            prompt_id=cmd.prompt_id
        )
        key_starts_with = "/".join(key_path.split("/")[:-1])

        return PromptLink(
            object_type=cmd.object_type,
            prompt_id=cmd.prompt_id,
            user_id=cmd.user_id,
            key_path=key_path,
            key_starts_with=key_starts_with,
        )

    @classmethod
    def parse(cls, path: str) -> Optional[PromptLink]:
        try:
            match = cls._pattern.match(path)
            if not match:
                return None

            groups = match.groupdict()
            key_starts_with = "/".join(path.split("/")[:-1])

            return PromptLink(
                object_type=groups["object_type"],
                user_id=groups["user_id"],
                prompt_id=groups["prompt_id"],
                key_path=path,
                key_starts_with=key_starts_with,
            )
        except ValidationError:
            return None