from dataclasses import dataclass
from datetime import timedelta
from enum import Enum
from functools import lru_cache

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class ModeEnum(str, Enum):
    DEVELOPMENT = "DEVELOPMENT"
    PRODUCTION = "PRODUCTION"
    TESTING = "TESTING"


@dataclass
class JWTConfig:
    issuer: str
    secret_key: str
    algorithm: str
    access_token_ttl: timedelta
    refresh_token_ttl: timedelta


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, env_file_encoding="utf-8")

    MODE: ModeEnum = ModeEnum.DEVELOPMENT
    BASE_URL: str = "http://127.0.0.1:8000"
    API_VERSION: str = "v1"
    API_V1_STR: str = f"/api/{API_VERSION}"
    PROJECT_NAME: str = "Backend"
    DEBUG: bool = True
    APP_PORT: int = 8000

    POSTGRES_USERNAME: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "database"
    POSTGRES_PORT: int = 5432
    POSTGRES_DATABASE: str = "postgres"

    JWT_SECRET_KEY: str = "secret"
    JWT_ISSUER: str = "FastAPI"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_TTL_SECONDS: int = 3600
    JWT_REFRESH_TOKEN_TTL_SECONDS: int = 86400

    @property
    def async_postgres_url(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            username=self.POSTGRES_USERNAME,
            password=self.POSTGRES_PASSWORD,
            path=self.POSTGRES_DATABASE,
        )

    @property
    def postgres_url(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgres",
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            username=self.POSTGRES_USERNAME,
            password=self.POSTGRES_PASSWORD,
            path=self.POSTGRES_DATABASE,
        )

    @property
    def jwt_config(self) -> JWTConfig:
        return JWTConfig(
            issuer=self.JWT_ISSUER,
            secret_key=self.JWT_SECRET_KEY,
            algorithm=self.JWT_ALGORITHM,
            access_token_ttl=timedelta(seconds=self.JWT_ACCESS_TOKEN_TTL_SECONDS),
            refresh_token_ttl=timedelta(seconds=self.JWT_REFRESH_TOKEN_TTL_SECONDS),
        )


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    return settings
