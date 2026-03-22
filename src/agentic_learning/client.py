import asyncio
import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamable_http_client

# Commented out: stdio configuration for local server process
# SERVER_PARAMS = StdioServerParameters(
#     command="python",
#     args=["-m", "agentic_learning.server"],
#     env={"PYTHONPATH": "src"},
# )

# HTTP endpoint URL for remote MCP server
SERVER_URL = "http://localhost:8000/mcp"

async def main() -> None:
    # Connect to MCP server via HTTP 
    async with streamable_http_client(SERVER_URL) as (read, write, _):
        # Establish MCP session over HTTP streams
        async with ClientSession(read, write) as session:
            # Initialize session and discover available tools
            await session.initialize()

            # Display welcome message and available commands
            print("\nConnected to MCP server.")
            print("Commands:")
            print("  search <query>")
            print("  details <book_id>")
            print("  exit\n")

            # Retrieve and display list of available tools
            tools_result = await session.list_tools()
            print("Available tools:")
            for tool in tools_result.tools:
                print(f"- {tool.name}: {tool.description}")
            print()

            # Interactive command loop
            while True:
                user_input = input(">> ").strip()

                # Handle exit command
                if user_input.lower() == "exit":
                    print("Exiting client.")
                    break

                # Handle search command
                if user_input.lower().startswith("search "):
                    # Extract query string
                    query = user_input[len("search "):].strip()
                    # Call search_books tool on server
                    result = await session.call_tool(
                        "search_books",
                        arguments={"query": query, "limit": 5},
                    )
                    # Print formatted JSON response
                    print(json.dumps(result.model_dump(), indent=2, default=str))
                    print()
                    continue

                # Handle details command
                if user_input.lower().startswith("details "):
                    # Extract book ID (ISBN or OLID)
                    book_id = user_input[len("details "):].strip()
                    # Call get_book_details tool on server
                    result = await session.call_tool(
                        "get_book_details",
                        arguments={"book_id": book_id},
                    )
                    # Print formatted JSON response
                    print(json.dumps(result.model_dump(), indent=2, default=str))
                    print()
                    continue

                # Handle invalid input
                print("Unknown command. Use: search <query>, details <book_id>, or exit.\n")

# Entry point: run async main function
if __name__ == "__main__":
    asyncio.run(main())