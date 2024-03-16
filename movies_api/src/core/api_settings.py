from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """
    Class to store fastapi project settings.
    """
    project_name: str = Field('Read-only API for online-cinema.')
    version: str = Field('1.0.0')
    redis_host: str = Field('127.0.0.1', env='MOVIES_REDIS_HOST')
    redis_port: int = Field(6379, env='MOVIES_REDIS_PORT')
    es_host: str = Field('127.0.0.1', env='MOVIES_ES_HOST')
    es_port: int = Field(9200, env='MOVIES_ES_PORT')
    log_format: str = Field('%(asctime)s - %(name)s - %(levelname)s - %(message)s', env='MOVIES_API_LOG_FORMAT')
    log_default_handlers: list = Field(['console', ], env='MOVIES_API_LOG_DEFAULT_HANDLERS')
    console_log_lvl: str = Field('DEBUG', env='MOVIES_API_CONSOLE_LOG_LVL')
    loggers_handlers_log_lvl: str = Field('INFO', env='MOVIES_API_LOGGERS_HANDLERS_LOG')
    unicorn_error_log_lvl: str = Field('INFO', env='MOVIES_API_UNICORN_ERROR_LOG_LVL')
    unicorn_access_log_lvl: str = Field('INFO', env='MOVIES_API_UNICORN_ACCESS_LOG_LVL')
    root_log_lvl: str = Field('INFO', env='MOVIES_API_ROOT_LOG_LVL')
    authjwt_algorithm: str = 'RS256'
    authjwt_public_key: str = Field(..., env='AUTHJWT_PUBLIC_KEY')

    class Config:
        env_file = '../.env'


settings = Settings()
