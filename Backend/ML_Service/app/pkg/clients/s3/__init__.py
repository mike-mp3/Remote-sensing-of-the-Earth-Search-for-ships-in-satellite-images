"""S3 Clients."""
from app.pkg.clients.s3.model import S3ModelClient
from app.pkg.clients.s3.path_strategies import PathStrategies
from app.pkg.clients.s3.prompter import S3PrompterClient
from app.pkg.settings import settings
from dependency_injector import containers, providers


class S3Clients(containers.DeclarativeContainer):
    """Container with S3 clients."""

    path_strategies: PathStrategies = providers.Container(PathStrategies)

    prompter: S3PrompterClient = providers.Factory(
        S3PrompterClient,
        base_url=settings.S3.URL,
        aws_access_key_id=settings.S3.RESULTER_USER_NAME,
        aws_secret_access_key=settings.S3.RESULTER_USER_PASSWORD,
        path_strategy=path_strategies.Prompter,
    )

    model: S3ModelClient = providers.Factory(
        S3ModelClient,
        base_url=settings.S3.URL,
        aws_access_key_id=settings.S3.RESULTER_USER_NAME,
        aws_secret_access_key=settings.S3.RESULTER_USER_PASSWORD,
        key_path=settings.ML_MODEL.S3_KEY_PATH,
    )
