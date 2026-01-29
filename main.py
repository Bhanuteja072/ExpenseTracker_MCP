import random
from fastmcp import FastMCP

mcp = FastMCP(name="expensetracker")

@mcp.tool
def roll_dice(n_dice : int = 1) -> list[int]:
    """Roll a specified number of six-sided dice and return the results."""
    return [random.randint(1, 6) for _ in range(n_dice)]

@mcp.tool
def add_two_num(a: int, b: int) -> int:
    """Add two numbers and return the result."""
    return a + b

if __name__ == "__main__":
    mcp.run()