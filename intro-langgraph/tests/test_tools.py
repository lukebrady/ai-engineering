"""Unit tests for tools.py module."""

import pytest
from pathlib import Path
from unittest.mock import patch, Mock
from tools import (
    web_search, create_file, read_file, update_file, delete_file, diff_files,
    SearchRequest, FileCreateRequest, FileReadRequest, FileUpdateRequest,
    FileDeleteRequest, FileDiffRequest, tools, get_tools
)


class TestWebSearch:
    """Test cases for web_search tool."""
    
    def test_web_search_success(self, mock_tavily_search):
        """Test successful web search."""
        request = SearchRequest(query="test query")
        result = web_search.invoke({"request": request})
        
        # Verify the search was called
        mock_tavily_search.invoke.assert_called_once_with("test query")
        
        # Verify the result contains expected data
        assert len(result) == 2
        assert result[0]["title"] == "Test Result 1"
        assert result[1]["url"] == "https://example.com/2"
    
    def test_web_search_with_complex_query(self, mock_tavily_search):
        """Test web search with complex query."""
        complex_query = "machine learning AND deep learning OR neural networks"
        request = SearchRequest(query=complex_query)
        
        web_search.invoke({"request": request})
        mock_tavily_search.invoke.assert_called_once_with(complex_query)
    
    def test_web_search_empty_query(self, mock_tavily_search):
        """Test web search with empty query."""
        request = SearchRequest(query="")
        web_search.invoke({"request": request})
        mock_tavily_search.invoke.assert_called_once_with("")


class TestCreateFile:
    """Test cases for create_file tool."""
    
    def test_create_file_success(self, temp_dir):
        """Test successful file creation."""
        file_path = temp_dir / "new_file.txt"
        content = "Hello, World!"
        request = FileCreateRequest(file_path=str(file_path), content=content)
        
        result = create_file.invoke({"request": request})
        
        # Verify the file was created
        assert file_path.exists()
        assert file_path.read_text(encoding='utf-8') == content
        assert "Successfully created file" in result
    
    def test_create_file_with_nested_directories(self, temp_dir):
        """Test file creation with nested directories."""
        file_path = temp_dir / "nested" / "dirs" / "file.txt"
        content = "Nested file content"
        request = FileCreateRequest(file_path=str(file_path), content=content)
        
        result = create_file.invoke({"request": request})
        
        # Verify the file and directories were created
        assert file_path.exists()
        assert file_path.read_text(encoding='utf-8') == content
        assert "Successfully created file" in result
    
    def test_create_file_already_exists(self, sample_file):
        """Test error when trying to create existing file."""
        request = FileCreateRequest(file_path=str(sample_file), content="new content")
        
        result = create_file.invoke({"request": request})
        
        assert "Error: File" in result
        assert "already exists" in result
    
    def test_create_file_empty_content(self, temp_dir):
        """Test creating file with empty content."""
        file_path = temp_dir / "empty_file.txt"
        request = FileCreateRequest(file_path=str(file_path), content="")
        
        result = create_file.invoke({"request": request})
        
        assert file_path.exists()
        assert file_path.read_text(encoding='utf-8') == ""
        assert "Successfully created file" in result
    
    def test_create_file_permission_error(self, temp_dir):
        """Test file creation with permission error."""
        # Try to create file in a non-writable location (simulate permission error)
        with patch('pathlib.Path.write_text', side_effect=PermissionError("Permission denied")):
            file_path = temp_dir / "permission_denied.txt"
            request = FileCreateRequest(file_path=str(file_path), content="test")
            
            result = create_file.invoke({"request": request})
            
            assert "Error creating file" in result
            assert "Permission denied" in result


class TestReadFile:
    """Test cases for read_file tool."""
    
    def test_read_file_success(self, sample_file, sample_file_content):
        """Test successful file reading."""
        request = FileReadRequest(file_path=str(sample_file))
        
        result = read_file.invoke({"request": request})
        
        assert f"Content of {sample_file}" in result
        assert sample_file_content in result
    
    def test_read_file_not_exists(self, nonexistent_file):
        """Test reading non-existent file."""
        request = FileReadRequest(file_path=str(nonexistent_file))
        
        result = read_file.invoke({"request": request})
        
        assert "Error: File" in result
        assert "does not exist" in result
    
    def test_read_file_is_directory(self, temp_dir):
        """Test reading a directory instead of file."""
        request = FileReadRequest(file_path=str(temp_dir))
        
        result = read_file.invoke({"request": request})
        
        assert "Error:" in result
        assert "is not a file" in result
    
    def test_read_file_permission_error(self, sample_file):
        """Test reading file with permission error."""
        with patch('pathlib.Path.read_text', side_effect=PermissionError("Permission denied")):
            request = FileReadRequest(file_path=str(sample_file))
            
            result = read_file.invoke({"request": request})
            
            assert "Error reading file" in result
            assert "Permission denied" in result


class TestUpdateFile:
    """Test cases for update_file tool."""
    
    def test_update_file_success(self, sample_file):
        """Test successful file update."""
        new_content = "Updated content"
        request = FileUpdateRequest(file_path=str(sample_file), content=new_content)
        
        result = update_file.invoke({"request": request})
        
        # Verify the file was updated
        assert sample_file.read_text(encoding='utf-8') == new_content
        assert "Successfully updated file" in result
    
    def test_update_file_not_exists(self, nonexistent_file):
        """Test updating non-existent file."""
        request = FileUpdateRequest(file_path=str(nonexistent_file), content="new content")
        
        result = update_file.invoke({"request": request})
        
        assert "Error: File" in result
        assert "does not exist" in result
        assert "Use create_file" in result
    
    def test_update_file_is_directory(self, temp_dir):
        """Test updating a directory instead of file."""
        request = FileUpdateRequest(file_path=str(temp_dir), content="content")
        
        result = update_file.invoke({"request": request})
        
        assert "Error:" in result
        assert "is not a file" in result
    
    def test_update_file_permission_error(self, sample_file):
        """Test updating file with permission error."""
        with patch('pathlib.Path.write_text', side_effect=PermissionError("Permission denied")):
            request = FileUpdateRequest(file_path=str(sample_file), content="new content")
            
            result = update_file.invoke({"request": request})
            
            assert "Error updating file" in result
            assert "Permission denied" in result


class TestDeleteFile:
    """Test cases for delete_file tool."""
    
    def test_delete_file_success(self, sample_file):
        """Test successful file deletion."""
        file_path_str = str(sample_file)
        request = FileDeleteRequest(file_path=file_path_str)
        
        # Verify file exists before deletion
        assert sample_file.exists()
        
        result = delete_file.invoke({"request": request})
        
        # Verify file was deleted
        assert not sample_file.exists()
        assert "Successfully deleted file" in result
    
    def test_delete_file_not_exists(self, nonexistent_file):
        """Test deleting non-existent file."""
        request = FileDeleteRequest(file_path=str(nonexistent_file))
        
        result = delete_file.invoke({"request": request})
        
        assert "Error: File" in result
        assert "does not exist" in result
    
    def test_delete_file_is_directory(self, temp_dir):
        """Test deleting a directory instead of file."""
        request = FileDeleteRequest(file_path=str(temp_dir))
        
        result = delete_file.invoke({"request": request})
        
        assert "Error:" in result
        assert "is not a file" in result
    
    def test_delete_file_permission_error(self, sample_file):
        """Test deleting file with permission error."""
        with patch('pathlib.Path.unlink', side_effect=PermissionError("Permission denied")):
            request = FileDeleteRequest(file_path=str(sample_file))
            
            result = delete_file.invoke({"request": request})
            
            assert "Error deleting file" in result
            assert "Permission denied" in result


class TestDiffFiles:
    """Test cases for diff_files tool."""
    
    def test_diff_files_success(self, sample_file, another_sample_file):
        """Test successful file diffing."""
        request = FileDiffRequest(
            file_path1=str(sample_file),
            file_path2=str(another_sample_file)
        )
        
        result = diff_files.invoke({"request": request})
        
        assert "Differences between" in result
        assert str(sample_file) in result
        assert str(another_sample_file) in result
        # Should contain diff markers
        assert ("---" in result or "+++" in result or "@@" in result)
    
    def test_diff_files_identical(self, sample_file, temp_dir, sample_file_content):
        """Test diffing identical files."""
        # Create identical file
        identical_file = temp_dir / "identical.txt"
        identical_file.write_text(sample_file_content, encoding='utf-8')
        
        request = FileDiffRequest(
            file_path1=str(sample_file),
            file_path2=str(identical_file)
        )
        
        result = diff_files.invoke({"request": request})
        
        assert "No differences found" in result
    
    def test_diff_files_first_not_exists(self, nonexistent_file, sample_file):
        """Test diffing when first file doesn't exist."""
        request = FileDiffRequest(
            file_path1=str(nonexistent_file),
            file_path2=str(sample_file)
        )
        
        result = diff_files.invoke({"request": request})
        
        assert "Error: File" in result
        assert "does not exist" in result
    
    def test_diff_files_second_not_exists(self, sample_file, nonexistent_file):
        """Test diffing when second file doesn't exist."""
        request = FileDiffRequest(
            file_path1=str(sample_file),
            file_path2=str(nonexistent_file)
        )
        
        result = diff_files.invoke({"request": request})
        
        assert "Error: File" in result
        assert "does not exist" in result
    
    def test_diff_files_custom_context_lines(self, sample_file, another_sample_file):
        """Test diffing with custom context lines."""
        request = FileDiffRequest(
            file_path1=str(sample_file),
            file_path2=str(another_sample_file),
            context_lines=5
        )
        
        result = diff_files.invoke({"request": request})
        
        assert "Differences between" in result
    
    def test_diff_files_directory_error(self, temp_dir, sample_file):
        """Test diffing when one path is a directory."""
        request = FileDiffRequest(
            file_path1=str(temp_dir),
            file_path2=str(sample_file)
        )
        
        result = diff_files.invoke({"request": request})
        
        assert "Error:" in result
        assert "is not a file" in result


class TestPydanticModels:
    """Test cases for Pydantic request models."""
    
    def test_search_request_valid(self):
        """Test valid SearchRequest creation."""
        request = SearchRequest(query="test query")
        assert request.query == "test query"
    
    def test_file_create_request_valid(self):
        """Test valid FileCreateRequest creation."""
        request = FileCreateRequest(file_path="/test/path", content="content")
        assert request.file_path == "/test/path"
        assert request.content == "content"
    
    def test_file_read_request_valid(self):
        """Test valid FileReadRequest creation."""
        request = FileReadRequest(file_path="/test/path")
        assert request.file_path == "/test/path"
    
    def test_file_update_request_valid(self):
        """Test valid FileUpdateRequest creation."""
        request = FileUpdateRequest(file_path="/test/path", content="new content")
        assert request.file_path == "/test/path"
        assert request.content == "new content"
    
    def test_file_delete_request_valid(self):
        """Test valid FileDeleteRequest creation."""
        request = FileDeleteRequest(file_path="/test/path")
        assert request.file_path == "/test/path"
    
    def test_file_diff_request_valid(self):
        """Test valid FileDiffRequest creation."""
        request = FileDiffRequest(file_path1="/path1", file_path2="/path2")
        assert request.file_path1 == "/path1"
        assert request.file_path2 == "/path2"
        assert request.context_lines == 3  # default value
    
    def test_file_diff_request_custom_context(self):
        """Test FileDiffRequest with custom context lines."""
        request = FileDiffRequest(
            file_path1="/path1", 
            file_path2="/path2", 
            context_lines=5
        )
        assert request.context_lines == 5


class TestToolsModule:
    """Test cases for module-level functionality."""
    
    def test_tools_dictionary_contains_all_tools(self):
        """Test that tools dictionary contains all expected tools."""
        expected_tools = {
            'web_search', 'create_file', 'read_file', 
            'update_file', 'delete_file', 'diff_files'
        }
        assert set(tools.keys()) == expected_tools
    
    def test_get_tools_returns_all_tools(self):
        """Test that get_tools returns all tool functions."""
        tool_list = get_tools()
        assert len(tool_list) == 6
        
        # Verify all tools are callable
        for tool in tool_list:
            assert callable(tool)
    
    def test_tools_have_descriptions(self):
        """Test that all tools have descriptions."""
        for tool_name, tool_func in tools.items():
            assert hasattr(tool_func, 'description')
            assert tool_func.description is not None
            assert len(tool_func.description) > 0
    
    def test_tools_have_proper_names(self):
        """Test that all tools have proper names."""
        for tool_name, tool_func in tools.items():
            assert hasattr(tool_func, 'name')
            assert tool_func.name == tool_name