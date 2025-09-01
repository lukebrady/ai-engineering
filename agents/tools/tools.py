import inspect
from datetime import datetime
from typing import Callable


class Tool:
    """
    A class representing a tool that can be used by the agent.

    Attributes:
        name (str): The name of the tool.
        description (str): A description of the tool.
        func (Callable): The function to call when the tool is used.
        args (list): The arguments to pass to the function.
        outputs (str): The return type(s) of the function.
    """

    def __init__(
        self,
        name: str,
        description: str,
        func: Callable,
        args: list,
        outputs: str,
    ):
        self.name = name
        self.description = description
        self.func = func
        self.args = args
        self.outputs = outputs

    def to_string(self):
        """
        Return a string representation of the tool,
        including its name, description, arguments, and outputs.
        """
        args_str = ", ".join([
            f"{arg_name}: {arg_type}" for arg_name, arg_type in self.args
        ])

        return (
            f"Tool Name: {self.name},"
            f" Description: {self.description},"
            f" Arguments: {args_str},"
            f" Outputs: {self.outputs}"
        )

    def __call__(self, *args, **kwargs):
        """
        Call the underlying function with the given arguments.
        """
        return self.func(*args, **kwargs)


def tool(func: Callable):
    """
    A decorator to convert a function into a tool.
    """
    # Get the function signature
    signature = inspect.signature(func)
    args = []
    for param in signature.parameters.values():
        annotation_name = (
            param.annotation.__name__
            if hasattr(param.annotation, "__name__")
            else str(param.annotation)
        )
        args.append((param.name, annotation_name))

    # Determine the return annotation
    return_annotation = signature.return_annotation
    if return_annotation is inspect._empty:
        outputs = "No return annotation"
    else:
        outputs = (
            return_annotation.__name__
            if hasattr(return_annotation, "__name__")
            else str(return_annotation)
        )

    # Use the function's docstring as the description (default if None)
    description = func.__doc__ or "No description provided."

    # The function name becomes the Tool name
    name = func.__name__

    # Return a new Tool instance
    return Tool(
        name=name,
        description=description,
        func=func,
        args=args,
        outputs=outputs,
    )

# Example tool
@tool
def get_current_time() -> str:
    """
    Get the current time.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if __name__ == "__main__":
    print(get_current_time.to_string())