from app.pkg.models import GeneratePromptLink, PromptLink
from .base import PathStrategy


class PrompterPathStrategy(PathStrategy[GeneratePromptLink, PromptLink]):
    _template: str = "{object_type}/user_{user_id}/prompt_{prompt_id}"

    @classmethod
    def generate_path(cls, cmd: GeneratePromptLink) -> PromptLink:
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
