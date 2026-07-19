from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # PostgreSQL
    postgres_host: str = Field(alias="POSTGRES_HOST")
    postgres_port: int = Field(alias="POSTGRES_PORT")
    postgres_db: str = Field(alias="POSTGRES_DB")
    postgres_user: str = Field(alias="POSTGRES_USER")
    postgres_password: str = Field(alias="POSTGRES_PASSWORD")

    # MinIO
    minio_endpoint: str = Field(alias="MINIO_ENDPOINT")
    minio_access_key: str = Field(alias="MINIO_ROOT_USER")
    minio_secret_key: str = Field(alias="MINIO_ROOT_PASSWORD")
    minio_secure: bool = Field(alias="MINIO_SECURE")
    minio_default_bucket: str = Field(alias="MINIO_DEFAULT_BUCKET")

    # Storage
    storage_mcp_host: str = Field(
        default="0.0.0.0",
        alias="STORAGE_MCP_HOST",
    )

    storage_mcp_port: int = Field(
        default=8001,
        alias="STORAGE_MCP_PORT",
    )

    # Upload
    upload_mcp_host: str = "0.0.0.0"
    upload_mcp_port: int = 8002

    @property
    def database_url(self) -> str:
        return (
            "postgresql+psycopg://"
            f"{self.postgres_user}:"
            f"{self.postgres_password}@"
            f"{self.postgres_host}:"
            f"{self.postgres_port}/"
            f"{self.postgres_db}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()