# MCP Demo — Pricing API + MCP Server

A demo showing how to combine a [FastAPI](https://fastapi.tiangolo.com/) REST API with an [MCP](https://modelcontextprotocol.io/) server using [FastMCP](https://github.com/jlowin/fastmcp), served from a single process.

## What it does

The app exposes pricing data for three product categories (`laptop`, `tablet`, `phone`) via:

- **REST endpoints** — standard HTTP routes for health checks and price lookups
- **MCP tools** — callable by AI agents/LLM clients over the MCP protocol

### REST endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/healthz` | Health check |
| GET | `/prices/{category}` | Raw prices for a category |

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
