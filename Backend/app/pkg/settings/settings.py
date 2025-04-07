"""Module for load settings form `.env` or if server running with parameter
`dev` from `.env.dev`"""
import pathlib
import typing
import urllib.parse
from functools import lru_cache

from dotenv import find_dotenv
from pydantic import PostgresDsn, RedisDsn, model_validator, field_validator
from pydantic.types import PositiveInt, SecretStr
from pydantic import AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from app.pkg.models.core.logger import LoggerLevel

__all__ = ["Settings", "get_settings"]


class _Settings(BaseSettings):
    """Base settings for all settings.

    Use double underscore for nested env variables.

    Examples:
        `.env` file should look like::

            TELEGRAM__TOKEN=...
            TELEGRAM__WEBHOOK_DOMAIN_URL=...

            LOGGER__PATH_TO_LOG="./src/logs"
            LOGGER__LEVEL="DEBUG"

            API_SERVER__HOST="127.0.0.1"
            API_SERVER__PORT=9191

    Warnings:
        In the case where a value is specified for the same Settings field in multiple
        ways, the selected value is determined as follows
        (in descending order of priority):

        1. Arguments passed to the Settings class initializer.
        2. Environment variables, e.g., my_prefix_special_function as described above.
        3. Variables loaded from a dotenv (.env) file.
        4. Variables loaded from the secrets directory.
        5. The default field values for the Settings model.

    See Also:
        https://docs.pydantic.dev/latest/usage/pydantic_settings/
    """

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        case_sensitive=True,
        env_nested_delimiter="__",
        extra='allow',
    )


class Postgresql(_Settings):
    """Postgresql settings."""

    HOST: str = "localhost"
    PORT: PositiveInt = 5432
    USER: str = "postgres"
    PASSWORD: SecretStr = SecretStr("postgres")
    DATABASE_NAME: str = "postgres"

    #: PositiveInt: Min count of connections in one pool to postgresql.
    MIN_CONNECTION: PositiveInt = 1
    #: PositiveInt: Max count of connections in one pool  to postgresql.
    MAX_CONNECTION: PositiveInt = 16

    #: str: Concatenation all settings for postgresql in one string. (DSN)
    #  Builds in `root_validator` method.
    DSN: typing.Optional[str] = None

    @model_validator(mode="after")
    def build_dsn(cls, values: "Postgresql"):  # pylint: disable=no-self-argument
        values.DSN = PostgresDsn.build(
            scheme="postgresql",
            username=f"{values.USER}",
            password=f"{urllib.parse.quote_plus(values.PASSWORD.get_secret_value())}",
            host=f"{values.HOST}",
            port=int(f"{values.PORT}"),
            path=f"{values.DATABASE_NAME}",
        )
        return values


class Redis(_Settings):
    """Redis settings."""

    HOST: str = "localhost"
    PORT: PositiveInt = 6379
    PASSWORD: SecretStr = SecretStr("redis")

    #: str: Concatenation all settings for Redis in one string. (DSN)
    #  Builds in `root_validator` method.
    DSN: typing.Optional[str] = None

    @model_validator(mode="after")
    def build_dsn(cls, values: "Redis"):  # pylint: disable=no-self-argument
        values.DSN = RedisDsn.build(
            scheme="redis",
            password=f"{urllib.parse.quote_plus(values.PASSWORD.get_secret_value())}",
            host=f"{values.HOST}",
            port=int(f"{values.PORT}"),
        )
        return values


class JWT(_Settings):
    """JWT settings."""

    #: str: Refresh token name in headers/body/cookies.
    REFRESH_TOKEN_NAME: str = "refresh_token"
    #: str: Access token name in headers/body/cookies.
    ACCESS_TOKEN_NAME: str = "access_token"
    #: SecretStr: Key for encrypt payload in jwt.
    SECRET_KEY: SecretStr = SecretStr("<KEY>")


class Logging(_Settings):
    """Logging settings."""

    #: StrictStr: Level of logging which outs in std
    LEVEL: LoggerLevel = LoggerLevel.DEBUG
    #: pathlib.Path: Path of saving logs on local storage.
    FOLDER_PATH: pathlib.Path = pathlib.Path("./src/logs")

    @field_validator("FOLDER_PATH")
    def __create_dir_if_not_exist(  # pylint: disable=unused-private-member, no-self-argument
        cls,
        v: pathlib.Path,
    ):
        """Create directory if not exist."""

        if not v.exists():
            v.mkdir(exist_ok=True, parents=True)
        return v


class SMTP(_Settings):
    """SMTP settings."""

    # --- SMTP SETTINGS ---
    HOST: str
    PORT: int = 587
    USE_TLS: bool = True

    # --- SENDER ACCOUNT SETTINGS --
    USERNAME: str
    PASSWORD: SecretStr


class S3(_Settings):
    """S3 settings."""

    # --- S3 SETTINGS ---
    URL: AnyUrl
    REQUESTER_USER_NAME: str
    REQUESTER_USER_PASSWORD: SecretStr


class APIServer(_Settings):
    """API settings."""

    # --- API SETTINGS ---
    INSTANCE_APP_NAME: str = "project_name"
    HOST: str = "project_host"
    PORT: PositiveInt = 5000

    # --- SECURITY SETTINGS ---
    X_ACCESS_TOKEN: SecretStr = SecretStr("secret")

    # --- OTHER SETTINGS ---
    LOGGER: Logging



class Settings(_Settings):
    """Server settings.

    Formed from `.env` or `.env.dev` if server running with parameter
    `dev`.
    """

    #: APIServer: API settings. Contains all settings for API.
    API: APIServer

    #: JWT: JWT settings.
    JWT: JWT

    #: Postgresql: Postgresql settings.
    POSTGRES: Postgresql

    #: Redis: Redis settings.
    REDIS: Redis

    #: SMTP: SMTP settings.
    SMTP: SMTP

    #: S3: S3 settings.
    S3: S3


# TODO: Возможно даже lru_cache не стоит использовать. Стоит использовать meta sigleton.
#   Для класса настроек. А инициализацию перенести в `def __init__`
@lru_cache
def get_settings(env_file: str = ".env") -> Settings:
    """Create settings instance."""
    return Settings(_env_file=find_dotenv(env_file))
