from __future__ import annotations

from fastmcp import FastMCP

from langgraph_mcp_playground.storage.service import StorageService

from langgraph_mcp_playground.storage.service import get_storage_service
from langgraph_mcp_playground.config.settings import get_settings

mcp = FastMCP("storage")

storage = get_storage_service()

settings = get_settings()

"""
Upload a file into object storage.

Args:
    filename: Name of the file.
    content: UTF-8 content.
    content_type: MIME type.
"""
@mcp.tool
def upload_file(
    filename: str,
    content: str,
    content_type: str = "text/plain",
):
    """
    Upload a file to object storage.
    """

    return storage.upload_bytes(
        object_key=filename,
        data=content.encode("utf-8"),
        content_type=content_type,
    )


@mcp.tool
def download_file(
    filename: str,
) -> bytes:
    """
    Download a file from object storage.
    """

    return storage.download_bytes(filename)


@mcp.tool
def delete_file(
    filename: str,
) -> None:
    """
    Delete a file from object storage.
    """

    storage.delete_object(filename)


@mcp.tool
def list_files():
    """
    List all stored files.
    """

    return storage.list_objects()


@mcp.tool
def stat_file(
    filename: str,
):
    """
    Return metadata about a stored object.
    """

    return storage.stat_object(filename)


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host=settings.storage_mcp_host,
        port=settings.storage_mcp_port,
    )