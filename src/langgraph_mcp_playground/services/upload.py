from __future__ import annotations

from sqlalchemy.orm import Session

from langgraph_mcp_playground.mcp.client import get_mcp_client
from langgraph_mcp_playground.models.upload import Upload
from langgraph_mcp_playground.repositories.upload import UploadRepository


class UploadService:
    """Business service for upload operations."""

    def __init__(self, session: Session) -> None:
        self._session = session
        self._repository = UploadRepository(session)
        self._mcp_client = get_mcp_client()

    async def upload(
        self,
        *,
        filename: str,
        content: str,
        content_type: str = "text/csv",
    ) -> Upload:
        """Upload a file and persist its metadata."""

        tools = await self._mcp_client.get_tools()

        upload_tool = next(
            tool
            for tool in tools
            if tool.name == "storage_upload_file"
        )

        storage_response = await upload_tool.ainvoke(
            {
                "filename": filename,
                "content": content,
                "content_type": content_type,
            }
        )

        upload = Upload(
            original_filename=filename,
            bucket=storage_response["bucket"],
            object_key=storage_response["object_key"],
            content_type=content_type,
            file_size=len(content.encode("utf-8")),
            #status=None,  # uses model default
        )

        try:
            self._repository.add(upload)
            self._session.commit()

        except Exception:
            self._session.rollback()

            delete_tool = next(
                tool
                for tool in tools
                if tool.name == "storage_delete_file"
            )

            await delete_tool.ainvoke(
                {
                    "filename": filename,
                }
            )

            raise

        return upload