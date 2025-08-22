import os
import difflib
from pathlib import Path
from typing import Optional, List
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain_tavily import TavilySearch

from utils import get_env

class SearchRequest(BaseModel):
    query: str = Field(description="The query to search for")

class FileCreateRequest(BaseModel):
    file_path: str = Field(description="The path where the file should be created")
    content: str = Field(description="The content to write to the file")

class FileReadRequest(BaseModel):
    file_path: str = Field(description="The path of the file to read")

class FileUpdateRequest(BaseModel):
    file_path: str = Field(description="The path of the file to update")
    content: str = Field(description="The new content to write to the file")

class FileDeleteRequest(BaseModel):
    file_path: str = Field(description="The path of the file to delete")

class FileDiffRequest(BaseModel):
    file_path1: str = Field(description="The path of the first file to compare")
    file_path2: str = Field(description="The path of the second file to compare")
    context_lines: Optional[int] = Field(default=3, description="Number of context lines to show in diff")

@tool
def web_search(request: SearchRequest):
    """
    Search the web for information if you determine that the user's query is not in your knowledge base.
    """
    print(f"Searching for {request.query}")
    search = TavilySearch(max_results=2)
    search_docs = search.invoke(request.query)
    return search_docs

@tool
def create_file(request: FileCreateRequest):
    """
    Create a new file with the specified content. Creates parent directories if they don't exist.
    """
    try:
        file_path = Path(request.file_path)
        # Create parent directories if they don't exist
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Check if file already exists
        if file_path.exists():
            return f"Error: File {request.file_path} already exists. Use update_file to modify existing files."
        
        # Write content to file
        file_path.write_text(request.content, encoding='utf-8')
        return f"Successfully created file: {request.file_path}"
    except Exception as e:
        return f"Error creating file {request.file_path}: {str(e)}"

@tool
def read_file(request: FileReadRequest):
    """
    Read the content of a file and return it.
    """
    try:
        file_path = Path(request.file_path)
        
        if not file_path.exists():
            return f"Error: File {request.file_path} does not exist."
        
        if not file_path.is_file():
            return f"Error: {request.file_path} is not a file."
        
        content = file_path.read_text(encoding='utf-8')
        return f"Content of {request.file_path}:\n\n{content}"
    except Exception as e:
        return f"Error reading file {request.file_path}: {str(e)}"

@tool
def update_file(request: FileUpdateRequest):
    """
    Update an existing file with new content. The file must already exist.
    """
    try:
        file_path = Path(request.file_path)
        
        if not file_path.exists():
            return f"Error: File {request.file_path} does not exist. Use create_file to create new files."
        
        if not file_path.is_file():
            return f"Error: {request.file_path} is not a file."
        
        # Write new content to file
        file_path.write_text(request.content, encoding='utf-8')
        return f"Successfully updated file: {request.file_path}"
    except Exception as e:
        return f"Error updating file {request.file_path}: {str(e)}"

@tool
def delete_file(request: FileDeleteRequest):
    """
    Delete a file from the filesystem.
    """
    try:
        file_path = Path(request.file_path)
        
        if not file_path.exists():
            return f"Error: File {request.file_path} does not exist."
        
        if not file_path.is_file():
            return f"Error: {request.file_path} is not a file."
        
        file_path.unlink()
        return f"Successfully deleted file: {request.file_path}"
    except Exception as e:
        return f"Error deleting file {request.file_path}: {str(e)}"

@tool
def diff_files(request: FileDiffRequest):
    """
    Compare two files and return a unified diff showing the differences.
    """
    try:
        file1_path = Path(request.file_path1)
        file2_path = Path(request.file_path2)
        
        # Check if both files exist
        if not file1_path.exists():
            return f"Error: File {request.file_path1} does not exist."
        
        if not file2_path.exists():
            return f"Error: File {request.file_path2} does not exist."
        
        if not file1_path.is_file():
            return f"Error: {request.file_path1} is not a file."
        
        if not file2_path.is_file():
            return f"Error: {request.file_path2} is not a file."
        
        # Read file contents
        content1 = file1_path.read_text(encoding='utf-8').splitlines(keepends=True)
        content2 = file2_path.read_text(encoding='utf-8').splitlines(keepends=True)
        
        # Generate unified diff
        diff = difflib.unified_diff(
            content1,
            content2,
            fromfile=request.file_path1,
            tofile=request.file_path2,
            n=request.context_lines
        )
        
        diff_text = ''.join(diff)
        
        if not diff_text:
            return f"No differences found between {request.file_path1} and {request.file_path2}"
        
        return f"Differences between {request.file_path1} and {request.file_path2}:\n\n{diff_text}"
    except Exception as e:
        return f"Error comparing files: {str(e)}"

# Tools to be used by LangChain
tools = {
    "web_search": web_search,
    "create_file": create_file,
    "read_file": read_file,
    "update_file": update_file,
    "delete_file": delete_file,
    "diff_files": diff_files
}

def get_tools():
    return list(tools.values())

if __name__ == "__main__":
    print("Available tools:")
    for tool_name, tool_func in tools.items():
        print(f"- {tool_name}: {tool_func.description}")