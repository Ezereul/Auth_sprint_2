from functools import lru_cache
from pathlib import Path

from async_fastapi_jwt_auth import AuthJWT
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).parent.parent.parent
ENV_PATH = PROJECT_ROOT / '.env'


class RedisSettings(BaseSettings):
    host: str = 'localhost'
    port: int = 6379

    model_config = SettingsConfigDict(env_prefix='AUTH_REDIS_', env_file=ENV_PATH, extra='ignore')


class LoggerSettings(BaseSettings):
    level: str
    format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    default_handlers: list = ['console']
    level_console: str = 'DEBUG'
    level_handlers: str = 'INFO'
    level_unicorn_errors: str = 'INFO'
    level_unicorn_access: str = 'INFO'
    level_root: str = 'INFO'

    model_config = SettingsConfigDict(env_prefix='AUTH_LOG_', env_file=ENV_PATH, extra='ignore')


class AuthSettings(BaseSettings):
    """
    More about config:
    https://sijokun.github.io/async-fastapi-jwt-auth/configuration/cookies/
    """

    authjwt_algorithm: str
    authjwt_public_key: str
    authjwt_private_key: str
    authjwt_access_token_expires: int
    authjwt_refresh_token_expires: int
    authjwt_cookie_secure: bool  # now False, recommended to set True in prod
    authjwt_cookie_csrf_protect: bool  # now False, recommended to set True in prod
    authjwt_cookie_samesite: str = 'lax'  # def: 'lax', available: 'none' (has broken auth on Chrome), 'strict' (idk)

    # Never change! Required to core functions.
    authjwt_token_location: set = {'cookies'}

    model_config = SettingsConfigDict(env_file=ENV_PATH, extra='ignore')


class YandexSettings(BaseSettings):
    auth_url: str
    client_id: str
    client_secret: str

    model_config = SettingsConfigDict(env_file=ENV_PATH, extra='ignore', env_prefix='AUTH_YANDEX_')


class Settings(BaseSettings):
    redis: RedisSettings = RedisSettings()
    logger: LoggerSettings = LoggerSettings()
    auth: AuthSettings = AuthSettings()
    yandex: YandexSettings = YandexSettings()
    database_url: str = 'postgresql+asyncpg://app:11111@localhost:5432/auth'
    enable_tracing: bool = False

    project_name: str = 'Authorization API'
    version: str = '1.0.0'

    model_config = SettingsConfigDict(env_file=ENV_PATH, env_prefix='AUTH_', extra='ignore')


settings = Settings()


@lru_cache
@AuthJWT.load_config
def get_auth_settings():
    return settings.auth
