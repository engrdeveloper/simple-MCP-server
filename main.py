# # server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="python-mcp-server")

@mcp.tool()
def add_numbers(a: int, b: int) -> str:
    """Add two numbers together."""
    return f"{a} + {b} = {a + b}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")

