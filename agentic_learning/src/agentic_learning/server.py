# Import type hints and async HTTP client
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

# Initialize MCP server named "book-finder"
mcp = FastMCP(name="book-finder")

# Define API endpoints for Open Library
OPEN_LIBRARY_SEARCH_URL = "https://openlibrary.org/search.json"
OPEN_LIBRARY_BOOKS_API_URL = "https://openlibrary.org/api/books"


# Transform raw search results into a clean, normalized format
def normalize_search_result(doc: dict[str, Any]) -> dict[str, Any]:
    # Extract cover image ID for building cover URL
    cover_id = doc.get("cover_i")
    # Return standardized book data with limited author/edition results
    return {
        "title": doc.get("title"),
        "authors": doc.get("author_name", [])[:3],  # Limit to top 3 authors
        "first_publish_year": doc.get("first_publish_year"),
        "edition_count": doc.get("edition_count"),
        "isbn_sample": doc.get("isbn", [])[:3],  # Limit to 3 ISBNs
        "edition_keys": doc.get("edition_key", [])[:3],  # Limit to 3 editions
        "work_key": doc.get("key"),
        "cover_url": (
            f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
            if cover_id
            else None
        ),
    }


# MCP tool: Search for books by title, author, or keywords
@mcp.tool()
async def search_books(query: str, limit: int = 5) -> dict[str, Any]:
    """Search for books by title, author, or general keywords."""
    # Enforce limit between 1-10 results
    limit = max(1, min(limit, 10))

    # Make async HTTP request to Open Library search API
    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.get(
            OPEN_LIBRARY_SEARCH_URL,
            params={"q": query, "limit": limit},
        )
        response.raise_for_status()  # Raise error if request fails
        data = response.json()

    # Extract and normalize search results
    docs = data.get("docs", [])
    results = [normalize_search_result(doc) for doc in docs[:limit]]

    # Return structured response with count and results
    return {
        "query": query,
        "count": len(results),
        "results": results,
    }


# MCP tool: Retrieve detailed information about a specific book
@mcp.tool()
async def get_book_details(book_id: str) -> dict[str, Any]:
    """Get book details using an ISBN or Open Library edition ID like OL7353617M."""
    # Clean input and determine identifier type (OLID or ISBN)
    cleaned = book_id.strip()
    bib_key = f"OLID:{cleaned}" if cleaned.upper().startswith("OL") else f"ISBN:{cleaned}"

    # Make async HTTP request to Open Library details API
    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.get(
            OPEN_LIBRARY_BOOKS_API_URL,
            params={
                "bibkeys": bib_key,
                "format": "json",
                "jscmd": "details",
            },
        )
        response.raise_for_status()
        data = response.json()

    # Check if book data was found
    book_data = data.get(bib_key)
    if not book_data:
        return {
            "book_id": book_id,
            "found": False,
            "message": "No book details found for the provided ID.",
        }

    # Extract nested details from response
    details = book_data.get("details", {})

    # Return structured book details
    return {
        "book_id": book_id,
        "found": True,
        "title": details.get("title"),
        "subtitle": details.get("subtitle"),
        "publish_date": details.get("publish_date"),
        "publishers": details.get("publishers", []),
        "number_of_pages": details.get("number_of_pages"),
        "subjects": details.get("subjects", [])[:10],  # Limit to 10 subjects
        "authors": details.get("authors", []),
    }


# Entry point: Start the MCP server
def main() -> None:
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()