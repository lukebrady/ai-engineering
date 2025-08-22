from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain_tavily import TavilySearch

from utils import get_env

import os
import io
import difflib
from typing import Optional, Literal


# -------------------- Web Search --------------------
class SearchRequest(BaseModel):
    query: str = Field(description="The query to search for")


@tool
def web_search(request: SearchRequest):
    """
    Search the web for information when the user's query requires up-to-date info.
    """
    print(f"Searching for {request.query}")
    # Tavily uses TAVILY_API_KEY under the hood
    _ = get_env("TAVILY_API_KEY")
    search = TavilySearch(max_results=5)
    search_docs = search.invoke(request.query)
    return search_docs


# -------------------- Filesystem Helpers --------------------
_WORKSPACE_ROOT = os.getenv("WORKSPACE_PATH", "/workspace")


def _resolve_path(path: str) -> str:
    """Resolve to an absolute path within the workspace root to avoid escaping the repo."""
    abs_path = os.path.abspath(path if os.path.isabs(path) else os.path.join(_WORKSPACE_ROOT, path))
    workspace_abs = os.path.abspath(_WORKSPACE_ROOT)
    if not abs_path.startswith(workspace_abs + os.sep) and abs_path != workspace_abs:
        raise ValueError(f"Path {abs_path} is outside workspace root {_WORKSPACE_ROOT}")
    return abs_path


# -------------------- File: Create --------------------
class FileCreateRequest(BaseModel):
    path: str = Field(description="Absolute path (preferred) or workspace-relative path to create")
    content: str = Field(description="Content to write to the file")
    exist_ok: bool = Field(default=False, description="If False, error when file exists. If True, overwrite.")


@tool
def file_create(request: FileCreateRequest):
    """
    Create a new file with the given content. Prefers absolute paths. Ensures path stays inside workspace.
    """
    target_path = _resolve_path(request.path)
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    if os.path.exists(target_path) and not request.exist_ok:
        raise FileExistsError(f"File already exists: {target_path}")
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(request.content)
    return {
        "action": "file_create",
        "path": target_path,
        "bytes_written": len(request.content.encode("utf-8")),
    }


# -------------------- File: Read --------------------
class FileReadRequest(BaseModel):
    path: str = Field(description="Absolute path (preferred) or workspace-relative path to read")
    start_line: Optional[int] = Field(default=None, description="One-indexed start line to slice, inclusive")
    end_line: Optional[int] = Field(default=None, description="One-indexed end line to slice, inclusive")
    max_bytes: int = Field(default=200_000, description="Max bytes to return to avoid huge payloads")


@tool
def file_read(request: FileReadRequest):
    """
    Read a file. Optionally slice by one-indexed line range. Returns content text.
    """
    target_path = _resolve_path(request.path)
    if not os.path.exists(target_path):
        raise FileNotFoundError(f"Not found: {target_path}")
    with open(target_path, "r", encoding="utf-8") as f:
        content = f.read()
    if request.start_line is not None or request.end_line is not None:
        lines = content.splitlines(keepends=True)
        start = (request.start_line - 1) if request.start_line and request.start_line > 0 else 0
        end = request.end_line if request.end_line and request.end_line > 0 else len(lines)
        content = "".join(lines[start:end])
    # Truncate if too large
    encoded = content.encode("utf-8")
    if len(encoded) > request.max_bytes:
        truncated = encoded[: request.max_bytes].decode("utf-8", errors="ignore")
        return {"action": "file_read", "path": target_path, "truncated": True, "content": truncated}
    return {"action": "file_read", "path": target_path, "truncated": False, "content": content}


# -------------------- File: Update --------------------
class FileUpdateRequest(BaseModel):
    path: str = Field(description="Absolute path (preferred) or workspace-relative path to update")
    content: str = Field(description="Content to write or append")
    mode: Literal["overwrite", "append"] = Field(default="overwrite", description="Overwrite or append")


@tool
def file_update(request: FileUpdateRequest):
    """
    Update a file by overwriting or appending content. Creates parent dirs if needed.
    """
    target_path = _resolve_path(request.path)
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    if request.mode == "overwrite":
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(request.content)
        written = len(request.content.encode("utf-8"))
    elif request.mode == "append":
        with open(target_path, "a", encoding="utf-8") as f:
            f.write(request.content)
        written = len(request.content.encode("utf-8"))
    else:
        raise ValueError("mode must be 'overwrite' or 'append'")
    return {"action": "file_update", "path": target_path, "mode": request.mode, "bytes_written": written}


# -------------------- File: Delete --------------------
class FileDeleteRequest(BaseModel):
    path: str = Field(description="Absolute path (preferred) or workspace-relative path to delete")
    missing_ok: bool = Field(default=False, description="If True, do not error when file does not exist")


@tool
def file_delete(request: FileDeleteRequest):
    """
    Delete a file.
    """
    target_path = _resolve_path(request.path)
    if not os.path.exists(target_path):
        if request.missing_ok:
            return {"action": "file_delete", "path": target_path, "deleted": False}
        else:
            raise FileNotFoundError(f"Not found: {target_path}")
    os.remove(target_path)
    return {"action": "file_delete", "path": target_path, "deleted": True}


# -------------------- File: Diff --------------------
class FileDiffRequest(BaseModel):
    path_a: str = Field(description="Absolute or workspace-relative path to the first file")
    path_b: str = Field(description="Absolute or workspace-relative path to the second file")
    context_lines: int = Field(default=3, description="Number of context lines for unified diff")


@tool
def file_diff(request: FileDiffRequest):
    """
    Return a unified diff between two files.
    """
    path_a = _resolve_path(request.path_a)
    path_b = _resolve_path(request.path_b)
    if not os.path.exists(path_a):
        raise FileNotFoundError(f"Not found: {path_a}")
    if not os.path.exists(path_b):
        raise FileNotFoundError(f"Not found: {path_b}")
    with open(path_a, "r", encoding="utf-8") as fa:
        a_lines = fa.readlines()
    with open(path_b, "r", encoding="utf-8") as fb:
        b_lines = fb.readlines()
    diff_iter = difflib.unified_diff(
        a_lines,
        b_lines,
        fromfile=path_a,
        tofile=path_b,
        n=request.context_lines,
    )
    buf = io.StringIO()
    for line in diff_iter:
        buf.write(line)
    return {"action": "file_diff", "from": path_a, "to": path_b, "diff": buf.getvalue()}


# Tools to be used by LangChain / LangGraph
_tools_registry = [
    web_search,
    file_create,
    file_read,
    file_update,
    file_delete,
    file_diff,
]


tools = {t.name: t for t in _tools_registry}


def get_tools():
    return list(_tools_registry)


if __name__ == "__main__":
    print([t.name for t in get_tools()])