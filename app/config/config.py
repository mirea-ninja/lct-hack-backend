from __future__ import annotations

from functools import lru_cache
from typing import Any, Dict, List, Optional

from dotenv import find_dotenv
from pydantic import BaseSettings, HttpUrl, PostgresDsn, validator


class AsyncPostgresDsn(PostgresDsn):
    allowed_schemes = {"postgres+asyncpg", "postgresql+asyncpg"}


class _Settings(BaseSettings):
    class Config:
        env_file_encoding = "utf-8"


class Config(_Settings):
    # Debug
    DEBUG: bool

    # Backend
    BACKEND_TTILE: str
    BACKEND_DESCRIPTION: str
    BACKEND_PREFIX: str

    BACKEND_HOST: str
    BACKEND_PORT: int
    BACKEND_RELOAD: bool

    # BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    BACKEND_CORS_ORIGINS: List = ["*"]

    # @validator("BACKEND_CORS_ORIGINS", pre=True)
    # def assemble_cors_origins(cls, v: str | List[str]) -> List[str] | str:
    #     if isinstance(v, str) and not v.startswith("["):
    #         return [i.strip() for i in v.split(",")]
    #     elif isinstance(v, (list, str)):
    #         return v
    #     raise ValueError(v)

    BACKEND_JWT_SECRET: str
    BACKEND_JWT_ALGORITHM: str
    BACKEND_JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int

    BACKEND_DADATA_TOKEN: str

    BACKEND_DISABLE_AUTH: bool
    BACKEND_DISABLE_FILE_SENDING: bool
    BACKEND_DISABLE_REGISTRATION: bool

    # Storage
    STORAGE_REGION: str
    STORAGE_ENDPOINT: HttpUrl
    STORAGE_ACCESS_KEY: str
    STORAGE_ACCESS_KEY_ID: str
    STORAGE_BUCKET_NAME: str
    STORAGE_FOLDER_NAME: str

    # Postgres
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    SQLALCHEMY_DATABASE_URI: Optional[AsyncPostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_async_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return AsyncPostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )


@lru_cache()
def get_config(env_file: str = ".env") -> Config:
    return Config(_env_file=find_dotenv(env_file))
