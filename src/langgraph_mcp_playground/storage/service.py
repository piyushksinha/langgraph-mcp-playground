from __future__ import annotations

from io import BytesIO

from minio.error import S3Error

from langgraph_mcp_playground.config.settings import get_settings
from langgraph_mcp_playground.storage.client import get_minio_client
from langgraph_mcp_playground.storage.schemas import (
    ObjectMetadata,
    StoredObject,
    UploadObjectResponse,
)

from functools import lru_cache


class StorageService:
    def __init__(self) -> None:
        settings = get_settings()

        self._client = get_minio_client()
        self._bucket = settings.minio_default_bucket

    def ensure_bucket_exists(self) -> None:
        if not self._client.bucket_exists(self._bucket):
            self._client.make_bucket(self._bucket)

    def upload_bytes(
        self,
        *,
        object_key: str,
        data: bytes,
        content_type: str = "application/octet-stream",
    ) -> UploadObjectResponse:
        self.ensure_bucket_exists()

        self._client.put_object(
            bucket_name=self._bucket,
            object_name=object_key,
            data=BytesIO(data),
            length=len(data),
            content_type=content_type,
        )

        return UploadObjectResponse(
            bucket=self._bucket,
            object_key=object_key,
        )

    def download_bytes(self, object_key: str) -> bytes:
        response = self._client.get_object(
            self._bucket,
            object_key,
        )

        try:
            return response.read()
        finally:
            response.close()
            response.release_conn()

    def delete_object(self, object_key: str) -> None:
        self._client.remove_object(
            self._bucket,
            object_key,
        )

    def stat_object(
        self,
        object_key: str,
    ) -> ObjectMetadata:
        stat = self._client.stat_object(
            self._bucket,
            object_key,
        )

        return ObjectMetadata(
            bucket=self._bucket,
            object_key=object_key,
            size=stat.size,
            etag=stat.etag,
            content_type=stat.content_type,
        )

    def list_objects(self) -> list[StoredObject]:
        return [
            StoredObject(object_key=obj.object_name)
            for obj in self._client.list_objects(
                self._bucket,
                recursive=True,
            )
        ]
    

@lru_cache
def get_storage_service() -> StorageService:
    return StorageService()