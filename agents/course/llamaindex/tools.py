from mcp.server.fastmcp import FastMCP

mcp = FastMCP("multiply")


@mcp.tool(name="add")
def add(a: int, b: int) -> int:
    """
    Add two numbers together.
    Example:
        add(2, 3) -> 5
    Args:
        a (int): The first number
        b (int): The second number
    Returns:
        int: The sum of the two numbers
    """
    return a + b


@mcp.tool(name="subtract")
def subtract(a: int, b: int) -> int:
    """
    Subtract two numbers together.
    Example:
        subtract(2, 3) -> -1
    Args:
        a (int): The first number
        b (int): The second number
    Returns:
        int: The difference of the two numbers
    """
    return a - b


# Define sample tool
@mcp.tool(name="multiply")
def multiply(a: int, b: int) -> int:
    """
    Multiply two numbers together.
    Example:
        multiply(2, 3) -> 6
    Args:
        a (int): The first number
        b (int): The second number
    Returns:
        int: The product of the two numbers
    """
    return a * b


# Define sample tool
@mcp.tool(name="divide")
def divide(a: int, b: int) -> int:
    """
    Divide two numbers together.
    Example:
        divide(2, 3) -> 0.6666666666666666
    Args:
        a (int): The first number
        b (int): The second number
    Returns:
        int: The quotient of the two numbers
    """
    return a / b


if __name__ == "__main__":
    mcp.run(transport="stdio")
