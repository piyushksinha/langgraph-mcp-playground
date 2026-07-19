from __future__ import annotations

import asyncio
import json

from langgraph_mcp_playground.mcp.client import get_mcp_client


def parse_text_result(result: list[dict]) -> str:
    """Extract the text payload from an MCP response."""

    if len(result) != 1:
        raise RuntimeError(f"Unexpected MCP response: {result}")

    block = result[0]

    if block["type"] != "text":
        raise RuntimeError(f"Unexpected content block: {block}")

    return block["text"]


def parse_json_result(result: list[dict]) -> dict:
    """Extract JSON returned by an MCP tool."""

    return json.loads(parse_text_result(result))


async def main() -> None:
    client = get_mcp_client()

    print("=" * 80)
    print("Connecting to Storage MCP...")
    print("=" * 80)

    tools = {
        tool.name: tool
        for tool in await client.get_tools()
    }

    print(f"Found {len(tools)} tool(s)\n")

    for name in sorted(tools):
        print(f"- {name}")

    filename = "customers.csv"

    content = (
        "name,email\n"
        "John Doe,john@example.com\n"
        "Jane Doe,jane@example.com\n"
    )

    print("\n" + "=" * 80)
    print("Uploading file...")
    print("=" * 80)

    upload_result = parse_json_result(
        await tools["storage_upload_file"].ainvoke(
            {
                "filename": filename,
                "content": content,
                "content_type": "text/csv",
            }
        )
    )

    print(upload_result)

    print("\n" + "=" * 80)
    print("Getting metadata...")
    print("=" * 80)

    stat_result = parse_json_result(
        await tools["storage_stat_file"].ainvoke(
            {
                "filename": filename,
            }
        )
    )

    print(stat_result)

    print("\n" + "=" * 80)
    print("Downloading file...")
    print("=" * 80)

    downloaded_content = parse_text_result(
        await tools["storage_download_file"].ainvoke(
            {
                "filename": filename,
            }
        )
    )

    print(downloaded_content)

    assert downloaded_content == content

    print("✓ Downloaded content matches uploaded content.")

    print("\n" + "=" * 80)
    print("Deleting file...")
    print("=" * 80)

    delete_result = await tools["storage_delete_file"].ainvoke(
        {
            "filename": filename,
        }
    )

    assert delete_result == []

    print("✓ File deleted successfully.")

    print("\n✅ Storage MCP integration test passed.")


if __name__ == "__main__":
    asyncio.run(main())