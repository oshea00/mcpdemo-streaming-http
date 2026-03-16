from contextlib import asynccontextmanager
from typing import Literal
from statistics import mean

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastmcp import FastMCP
from fastmcp.utilities.lifespan import combine_lifespans

# ---------------------------------
# Example backing data / service
# ---------------------------------

PRICES = {
    "laptop": [1199.0, 1499.0, 999.0, 1799.0],
    "tablet": [499.0, 699.0, 899.0],
    "phone": [799.0, 999.0, 1199.0, 899.0],
}


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    # Put real startup/shutdown work here:
    # - DB pool creation
    # - config/secrets load
    # - telemetry init
    print("FastAPI startup")
    yield
    print("FastAPI shutdown")


# ---------------------------------
# MCP server
# ---------------------------------

mcp = FastMCP("pricing-tools")


@mcp.tool
def get_categories() -> list[str]:
    """Return all available pricing categories."""
    return list(PRICES.keys())


@mcp.tool
def analyze_pricing(category: Literal["laptop", "tablet", "phone"]) -> dict:
    """Return simple pricing statistics for a category."""
    values = PRICES[category]
    return {
        "category": category,
        "count": len(values),
        "avg_price": round(mean(values), 2),
        "min_price": min(values),
        "max_price": max(values),
    }


@mcp.tool
def discount_price(price: float, percent: float) -> dict:
    """Apply a percentage discount to a price."""
    discounted = round(price * (1 - percent / 100.0), 2)
    return {
        "original_price": price,
        "discount_percent": percent,
        "discounted_price": discounted,
    }


@mcp.resource("config://service-info")
def service_info() -> str:
    return "Pricing MCP service v1.0"


# Build the MCP ASGI app using modern HTTP transport semantics.
# Mounted under /mcp below.
mcp_app = mcp.http_app(path="/")


# ---------------------------------
# FastAPI app
# ---------------------------------

app = FastAPI(
    title="Pricing API + MCP",
    lifespan=combine_lifespans(app_lifespan, mcp_app.lifespan),
)


@app.get("/healthz")
async def healthz():
    return JSONResponse({"ok": True})


@app.get("/prices/{category}")
async def get_prices(category: str):
    values = PRICES.get(category)
    if values is None:
        return JSONResponse({"error": "unknown category"}, status_code=404)
    return {"category": category, "prices": values}


# Mount MCP under /mcp
app.mount("/mcp", mcp_app)

