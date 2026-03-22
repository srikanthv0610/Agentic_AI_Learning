import asyncio
import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


SERVER_PARAMS = StdioServerParameters(
    command="python",
    args=["-m", "agentic_learning.server"],
    env={"PYTHONPATH": "src"},
)


async def main() -> None:
    async with stdio_client(SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            print("\nConnected to MCP server.")
            print("Commands:")
            print("  search <query>")
            print("  details <book_id>")
            print("  exit\n")

            tools_result = await session.list_tools()
            print("Available tools:")
            for tool in tools_result.tools:
                print(f"- {tool.name}: {tool.description}")
            print()

            while True:
                user_input = input(">> ").strip()

                if user_input.lower() == "exit":
                    print("Exiting client.")
                    break

                if user_input.lower().startswith("search "):
                    query = user_input[len("search "):].strip()
                    result = await session.call_tool(
                        "search_books",
                        arguments={"query": query, "limit": 5},
                    )
                    print(json.dumps(result.model_dump(), indent=2, default=str))
                    print()
                    continue

                if user_input.lower().startswith("details "):
                    book_id = user_input[len("details "):].strip()
                    result = await session.call_tool(
                        "get_book_details",
                        arguments={"book_id": book_id},
                    )
                    print(json.dumps(result.model_dump(), indent=2, default=str))
                    print()
                    continue

                print("Unknown command. Use: search <query>, details <book_id>, or exit.\n")


if __name__ == "__main__":
    asyncio.run(main())