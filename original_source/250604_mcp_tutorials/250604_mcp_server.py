import numpy as np
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("Math") # name of MCP server

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def substraction(a: int, b: int) -> int:
    """get result of 'a minus b'"""
    return a - b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

@mcp.tool()
def division(a: int, b: int) -> int:
    """Multiply two numbers"""
    try: 
        return a / b
    except ZeroDivisionError:
        raise np.inf
    
if __name__ == "__main__":
    mcp.run(transport="stdio")