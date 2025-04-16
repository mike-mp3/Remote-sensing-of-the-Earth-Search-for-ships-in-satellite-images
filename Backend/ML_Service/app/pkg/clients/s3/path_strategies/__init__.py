"""S3 Path Strategies."""

from app.pkg.clients.s3.path_strategies.prompter import PrompterPathStrategy
from dependency_injector import containers, providers


class PathStrategies(containers.DeclarativeContainer):
    """Container with S3 Path Strategies."""

    Prompter = providers.Object(PrompterPathStrategy)
