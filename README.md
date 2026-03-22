Agentic Learning MCP Server

A local Model Context Protocol (MCP) learning project built with Python, FastMCP, and the Open Library API.

This project includes:
	•	an MCP server that exposes book search and book detail lookup tools
	•	an MCP client that connects to the server over a local HTTP MCP endpoint
	•	a simple interactive CLI workflow for testing MCP end to end on your machine

Features
	•	MCP server built with FastMCP
	•	Local HTTP endpoint using Streamable HTTP transport
	•	MCP client that connects to the local server
	•	Book search using the Open Library Search API
	•	Book details lookup using the Open Library Books API
	•	Simple interactive CLI client for local testing

Architecture

+-------------------+        HTTP MCP         +---------------------------+
| MCP Client        |  <------------------>   | MCP Server                |
| client.py         |                         | server.py                 |
| interactive CLI   |                         | FastMCP tools             |
+-------------------+                         +---------------------------+
                                                        |
                                                        |
                                                        v
                                            +---------------------------+
                                            | Open Library APIs         |
                                            | Search API                |
                                            | Books API                 |
                                            +---------------------------+

Project Structure

agentic_learning/
├── .venv/
├── src/
│   └── agentic_learning/
│       ├── __init__.py
│       ├── server.py
│       └── client.py
├── requirements.txt
├── LICENSE
└── README.md

Prerequisites
	•	Python 3.11+
	•	pip
	•	VS Code or any local terminal

Setup

1. Create and activate a virtual environment

python3 -m venv .venv
source .venv/bin/activate

2. Install dependencies

pip install mcp httpx

3. Verify installation

pip list

You should see mcp and httpx installed.

Running the MCP Server

Run the server from the project root:

PYTHONPATH=src python -m agentic_learning.server

The server starts locally and exposes an MCP endpoint at:

http://localhost:8000/mcp

Leave this terminal running while using the client.

Running the MCP Client

Open a second terminal, activate the same virtual environment, and run:

PYTHONPATH=src python -m agentic_learning.client

Client Commands

Once the client starts, you can use commands like:

search clean code
details 9780132350884
exit

Example Commands

Search for books:

search dune

Get details for a book by ISBN:

details 9780132350884

Get details for a book by Open Library edition ID:

details OL7353617M

MCP Tools Exposed by the Server

search_books

Searches Open Library for books by title, author, or keywords.

Arguments:
	•	query (str): search term
	•	limit (int, optional): number of results to return

get_book_details

Gets book details using either an ISBN or an Open Library edition ID.

Arguments:
	•	book_id (str): ISBN or OLID

APIs Used
	•	Open Library Search API
	•	Open Library Books API

Typical Local Workflow

Terminal 1

source .venv/bin/activate
PYTHONPATH=src python -m agentic_learning.server

Terminal 2

source .venv/bin/activate
PYTHONPATH=src python -m agentic_learning.client

Development Notes
	•	The server uses MCP Streamable HTTP transport.
	•	The client connects to the local endpoint instead of spawning the server process.
	•	Keep server and client running in separate terminals during local development.
	•	If you switch back to a stdio-based server later, avoid writing normal print() output to stdout from the server process.
	•	Structured logging and input validation are good next improvements.

Troubleshooting

ModuleNotFoundError: No module named 'agentic_learning'

Run commands from the project root and include:

PYTHONPATH=src

Port already in use

Stop the old server process and restart it.

Client cannot connect to server

Make sure the server is already running at:

http://localhost:8000/mcp

Missing dependencies

Reinstall with:

pip install mcp httpx

Future Improvements
	•	Add MCP resources in addition to tools
	•	Add input validation and clearer error handling
	•	Add caching for repeated book lookups
	•	Add a health endpoint
	•	Dockerize the app
	•	Add tests for server tools and client behavior
	•	Add an LLM-powered client on top of the MCP client layer

License

This project is licensed under the MIT License. See the LICENSE file for details.