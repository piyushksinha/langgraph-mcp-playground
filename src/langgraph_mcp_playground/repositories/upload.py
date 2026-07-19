from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from langgraph_mcp_playground.models.upload import Upload


class UploadRepository:
    """Repository for Upload persistence operations."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, upload: Upload) -> Upload:
        """Persist a new Upload entity."""
        self._session.add(upload)
        self._session.flush()
        self._session.refresh(upload)
        return upload

    def get(self, upload_id: UUID) -> Upload | None:
        """Return an Upload by its primary key."""
        return self._session.get(Upload, upload_id)

    def get_by_object_key(self, object_key: str) -> Upload | None:
        """Return an Upload by its object key."""
        stmt = select(Upload).where(Upload.object_key == object_key)
        return self._session.scalar(stmt)

    def delete(self, upload: Upload) -> None:
        """Delete an Upload entity."""
        self._session.delete(upload)
        self._session.flush()