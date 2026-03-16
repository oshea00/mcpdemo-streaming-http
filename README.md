# MCP Demo — FastMCP hosted in FastAPI

A demo showing how to host a [FastMCP](https://github.com/jlowin/fastmcp) server inside a [FastAPI](https://fastapi.tiangolo.com/) app, served from a single process over the streamable-HTTP transport.

## What it does

The app exposes pricing tools for three product categories (`laptop`, `tablet`, `phone`) via MCP, mounted at `/mcp`. A `/healthz` endpoint is included for operational checks.

### MCP tools (mounted at `/mcp`)

| Tool | Description |
|------|-------------|
| `get_categories` | List all available pricing categories |
| `analyze_pricing` | Min/max/avg statistics for a category |
| `discount_price` | Apply a percentage discount to a price |

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)

## Starting the server

```bash
./start.sh
```

This runs:

```bash
uv run uvicorn main:app --host 0.0.0.0 --port 5000
```

The server listens on `http://localhost:5000`.

## MCP client configuration

Point your MCP client at the streamable-HTTP transport endpoint:

```
http://localhost:5000/mcp
```
