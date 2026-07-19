from __future__ import annotations

from functools import lru_cache
from typing import TypeAlias

from langchain_mcp_adapters.client import (
    MultiServerMCPClient,
    SSEConnection,
    StdioConnection,
    StreamableHttpConnection,
    WebsocketConnection,
)

from langgraph_mcp_playground.config.settings import get_settings

Connection: TypeAlias = (
    StdioConnection
    | SSEConnection
    | StreamableHttpConnection
    | WebsocketConnection
)


def _connections() -> dict[str, Connection]:
    """Build MCP server connection configuration."""

    settings = get_settings()

    return {
        "storage": {
            "transport": "streamable_http",
            "url": (
                f"http://{settings.storage_mcp_host}:"
                f"{settings.storage_mcp_port}/mcp"
            ),
        },
    }


@lru_cache(maxsize=1)
def get_mcp_client() -> MultiServerMCPClient:
    """Return a shared MCP client."""

    return MultiServerMCPClient(
        connections=_connections(),     # type: ignore[arg-type]
        tool_name_prefix=True,
    )