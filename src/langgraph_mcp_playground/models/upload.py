from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import BigInteger
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from langgraph_mcp_playground.database.base import Base
from langgraph_mcp_playground.models.enums import UploadStatus
from langgraph_mcp_playground.models.mixins import TimestampMixin


class Upload(TimestampMixin, Base):
    __tablename__ = "uploads"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    original_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    bucket: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    object_key: Mapped[str] = mapped_column(
        String(512),
        nullable=False,
    )

    content_type: Mapped[str | None] = mapped_column(
        String(100),
    )

    file_size: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    checksum: Mapped[str | None] = mapped_column(
        String(64),
    )

    status: Mapped[UploadStatus] = mapped_column(
        Enum(
            UploadStatus,
            name="upload_status",
        ),
        nullable=False,
        default=UploadStatus.RECEIVED,
    )

    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )