"""
Simple MCP Server
"""

from mcp.server.fastmcp import FastMCP
from pydantic import Field

mcp = FastMCP("Simple MCP Server", port=3000, stateless_http=True, debug=True)


@mcp.tool(
    title="Add Numbers",
    description="Add two numbers together",
)
def add_numbers(
    a: int = Field(description="First number to add"),
    b: int = Field(description="Second number to add")
) -> str:
    """Add two numbers together."""
    return f"{a} + {b} = {a + b}"


if __name__ == "__main__":
    mcp.run(transport="streamable-http", stateless_http=True, debug=True)

