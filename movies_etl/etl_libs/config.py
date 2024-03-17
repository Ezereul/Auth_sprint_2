from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = '../../.env'


@lru_cache
def get_settings():
    return Settings()


class PostgresSettings(BaseSettings):
    database: str
    user: str
    password: str
    host: str
    port: int

    model_config = SettingsConfigDict(env_prefix='MOVIES_PG_', env_file=ENV_FILE, env_file_encoding='utf-8')


class ElasticSettings(BaseSettings):
    host: str
    port: int
    indexes: list

    model_config = SettingsConfigDict(env_prefix='MOVIES_ES_', env_file=ENV_FILE, env_file_encoding='utf-8')


class LoggerSettings(BaseSettings):
    path: str
    level: str
    format: str

    model_config = SettingsConfigDict(env_prefix='MOVIES_ETL_LOG_', env_file=ENV_FILE, env_file_encoding='utf-8')


class Settings(BaseSettings):
    postgres: PostgresSettings = PostgresSettings()
    elastic: ElasticSettings = ElasticSettings()
    logger: LoggerSettings = LoggerSettings()
    interval: int

    model_config = SettingsConfigDict(env_file=ENV_FILE, env_prefix='MOVIES_ETL_', env_file_encoding='utf-8', extra='ignore')
