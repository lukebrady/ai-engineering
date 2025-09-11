import os
from subprocess import getoutput

from pydantic import BaseModel


class WriteFileArgs(BaseModel):
    file_path: str
    content: str


class ReadFileArgs(BaseModel):
    file_path: str


class DeleteFileArgs(BaseModel):
    file_path: str


class CreateDirectoryArgs(BaseModel):
    directory_path: str

class DeleteDirectoryArgs(BaseModel):
    directory_path: str


class OpenTofuArgs(BaseModel):
    directory_path: str
    command: str


def write_file(file_path: str, content: str) -> str:
    """
    Write to a file.
    """
    with open(file_path, "w") as f:
        f.write(content)
    return "File written successfully."


def read_file(file_path: str) -> str:
    """
    Read a file.
    """
    with open(file_path, "r") as f:
        return f.read()


def delete_file(file_path: str) -> str:
    """
    Delete a file.
    """
    os.remove(file_path)
    return "File deleted successfully."


def create_directory(directory_path: str) -> str:
    """
    Create a directory.
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        return "Directory created successfully."
    else:
        return "Directory already exists."

def delete_directory(directory_path: str) -> str:
    """
    Delete a directory.
    """
    if os.path.exists(directory_path):
        os.rmdir(directory_path)
        return "Directory deleted successfully."
    else:
        return "Directory does not exist."


def opentofu(directory_path: str, command: str) -> str:
    """
    Execute an OpenTofu command.
    """
    os.chdir(directory_path)
    result = getoutput(f"tofu {command}")
    if result:
        return "OpenTofu command executed successfully."
    else:
        return "OpenTofu command executed failed."


write_file_schema = WriteFileArgs.model_json_schema()
read_file_schema = ReadFileArgs.model_json_schema()
delete_file_schema = DeleteFileArgs.model_json_schema()
create_directory_schema = CreateDirectoryArgs.model_json_schema()
delete_directory_schema = DeleteDirectoryArgs.model_json_schema()
opentofu_schema = OpenTofuArgs.model_json_schema()
tool_definitions = [
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write to a file.",
            "parameters": write_file_schema,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a file.",
            "parameters": read_file_schema,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_file",
            "description": "Delete a file.",
            "parameters": delete_file_schema,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_directory",
            "description": "Create a directory.",
            "parameters": create_directory_schema,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_directory",
            "description": "Delete a directory.",
            "parameters": delete_directory_schema,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "opentofu",
            "description": "Execute an OpenTofu command.",
            "parameters": opentofu_schema,
        },
    },
]

tools_map = {
    "write_file": write_file,
    "read_file": read_file,
    "delete_file": delete_file,
    "create_directory": create_directory,
    "delete_directory": delete_directory,
    "opentofu": opentofu,
}
