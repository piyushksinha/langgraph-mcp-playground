from __future__ import annotations

from fastmcp import FastMCP

from langgraph_mcp_playground.config.settings import get_settings
from langgraph_mcp_playground.database.session import SessionLocal
from langgraph_mcp_playground.services.upload import UploadService

settings = get_settings()

mcp = FastMCP("upload")


@mcp.tool
async def upload_csv(
    filename: str,
    content: str,
    content_type: str = "text/csv",
) -> dict:
    """
    Upload a CSV file and persist its metadata.
    """

    with SessionLocal() as session:
        service = UploadService(session)

        upload = await service.upload(
            filename=filename,
            content=content,
            content_type=content_type,
        )

        return {
            "upload_id": str(upload.id),
            "filename": upload.original_filename,
            "status": upload.status.value,
        }


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host=settings.upload_mcp_host,
        port=settings.upload_mcp_port,
    )