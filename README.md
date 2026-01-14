# CanvasMCP-Py

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server for the Canvas Learning Management System (LMS), written in Python.

This server allows AI agents to interact with Canvas to retrieve course information, assignments, modules, files, and more.

## Features

- **Courses**: List and get details for courses.
- **Assignments**: List assignments, quizzes, and get verification details.
- **Content**: Access Modules, Pages, Folders, and Files.
- **Social**: Access Announcements, Discussion Topics, To-Do items, and Calendar events.
- **File Processing**: Automatically extracts text from PDF files.
- **Authentication**: Secure Bearer token authentication for server access.

## Prerequisites

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) (recommended for dependency management)
- A valid Canvas API Token (generate this in your Canvas Account Settings)

## Configuration

1.  Clone the repository.
2.  Copy `.env.example` to `.env`:
    ```bash
    cp .env.example .env
    ```
3.  Edit `.env` and configure your credentials:

    ```ini
    # Your Canvas instance URL (e.g., https://canvas.instructure.com)
    CANVAS_BASE_URL=https://canvas.your-institution.edu
    
    # Your Canvas API Token
    CANVAS_TOKEN=your_canvas_api_token
    
    # Token to secure THIS server (clients must provide this)
    MCP_SERVER_TOKEN=your_secret_server_token
    ```

## Development Setup

We recommend using `uv` for fast dependency management.

1.  **Install Dependencies**:
    ```bash
    uv sync
    ```

2.  **Run the Server**:
    ```bash
    uv run python -m src.server
    ```
    The server will start on `http://127.0.0.1:2222/mcp` (using SSE transport).

3.  **Verify Connection**:
    You can use the included test client to verify the connection and tool functionality:
    ```bash
    uv run python test_client.py
    ```

## Deployment (Docker)

You can easily deploy the server using Docker Compose.

1.  **Start the Container**:
    ```bash
    docker compose up --build -d
    ```
    This will start the server on port `2222`.

2.  **Check Logs**:
    ```bash
    docker compose logs -f
    ```

## Authentication

The server is protected by Bearer Token Authentication. Any client connecting to the SSE endpoint must provide the token configured in `MCP_SERVER_TOKEN`.

**Header**:
```
Authorization: Bearer <your_mcp_server_token>
```

**Endpoint**: `http://localhost:2222/mcp`

## Troubleshooting

### 403 Forbidden on `list_files`
Some courses hide the "Files" tab, which causes the `list_files` tool to return a `403 Forbidden` error.

**Workaround**: Use the `list_modules` tool with `include=['items']`.
- This will list all module items, including files.
- The server can successfully access and download files found within modules, even if the general file list is restricted.
