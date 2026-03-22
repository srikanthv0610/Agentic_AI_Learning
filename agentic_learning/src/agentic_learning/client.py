import asyncio
import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Configure how to launch the MCP server process in stdio mode.
# - command: "python"
# - args: run module agentic_learning.server
# - env: make sure Python can find src packages
SERVER_PARAMS = StdioServerParameters(
    command="python",
    args=["-m", "agentic_learning.server"],
    env={"PYTHONPATH": "src"},
)


async def main() -> None:
    # Start stdio-based client for server process
    async with stdio_client(SERVER_PARAMS) as (read, write):
        # Open an MCP session over the stdio pipes
        async with ClientSession(read, write) as session:
            await session.initialize()  # handshake + tool discovery

            print("\nConnected to MCP server.\n")

            # List exposed tools from server
            tools_result = await session.list_tools()
            print("Available tools:")
            for tool in tools_result.tools:
                # Each tool has name/description
                print(f"- {tool.name}: {tool.description}")

            # Call search_books tool with a query and limit
            print("\nCalling search_books...\n")
            search_result = await session.call_tool(
                "search_books",
                arguments={"query": "clean code", "limit": 3},
            )
            # print structured result using JSON formatting
            print(json.dumps(search_result.model_dump(), indent=2, default=str))

            # Call get_book_details tool with an ISBN
            print("\nCalling get_book_details...\n")
            details_result = await session.call_tool(
                "get_book_details",
                arguments={"book_id": "9780132350884"},
            )
            print(json.dumps(details_result.model_dump(), indent=2, default=str))


if __name__ == "__main__":
    asyncio.run(main())