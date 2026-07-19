from __future__ import annotations

from functools import lru_cache

from minio import Minio

from langgraph_mcp_playground.config.settings import get_settings


class MinioClient:
    """Wrapper around the MinIO SDK."""

    def __init__(self) -> None:
        settings = get_settings()

        self._client = Minio(
            endpoint=settings.minio_endpoint,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            secure=settings.minio_secure,
        )

    @property
    def client(self) -> Minio:
        return self._client


@lru_cache
def get_minio_client() -> Minio:
    """Return a singleton MinIO client."""
    return MinioClient().client