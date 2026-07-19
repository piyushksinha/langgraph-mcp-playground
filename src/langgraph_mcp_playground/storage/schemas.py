from __future__ import annotations

from pydantic import BaseModel


class UploadObjectResponse(BaseModel):
    bucket: str
    object_key: str


class ObjectMetadata(BaseModel):
    bucket: str
    object_key: str
    size: int
    content_type: str | None = None
    etag: str


class StoredObject(BaseModel):
    object_key: str