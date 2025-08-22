"""Pytest configuration and fixtures for the test suite."""

import os
import tempfile
import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from typing import Generator


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for testing file operations."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def sample_file_content() -> str:
    """Sample file content for testing."""
    return "This is a test file.\nLine 2\nLine 3"


@pytest.fixture
def sample_file(temp_dir: Path, sample_file_content: str) -> Path:
    """Create a sample file for testing."""
    file_path = temp_dir / "sample.txt"
    file_path.write_text(sample_file_content, encoding='utf-8')
    return file_path


@pytest.fixture
def another_sample_file(temp_dir: Path) -> Path:
    """Create another sample file for diff testing."""
    file_path = temp_dir / "sample2.txt"
    content = "This is a different test file.\nLine 2 modified\nLine 3"
    file_path.write_text(content, encoding='utf-8')
    return file_path


@pytest.fixture
def nonexistent_file(temp_dir: Path) -> Path:
    """Path to a non-existent file for testing error cases."""
    return temp_dir / "nonexistent.txt"


@pytest.fixture
def mock_tavily_search():
    """Mock Tavily search for web search testing."""
    with patch('tools.TavilySearch') as mock_search_class:
        mock_search_instance = Mock()
        mock_search_class.return_value = mock_search_instance
        mock_search_instance.invoke.return_value = [
            {
                "title": "Test Result 1",
                "content": "This is test content 1",
                "url": "https://example.com/1"
            },
            {
                "title": "Test Result 2", 
                "content": "This is test content 2",
                "url": "https://example.com/2"
            }
        ]
        yield mock_search_instance


@pytest.fixture
def mock_env_vars():
    """Mock environment variables for testing."""
    env_vars = {
        "OPENAI_API_KEY": "test_openai_key",
        "TAVILY_API_KEY": "test_tavily_key",
        "LANGSMITH_API_KEY": "test_langsmith_key",
        "LANGSMITH_TRACING_V2": "true",
        "LANGSMITH_PROJECT": "test_project"
    }
    with patch.dict(os.environ, env_vars):
        yield env_vars


@pytest.fixture
def mock_chat_openai():
    """Mock ChatOpenAI for testing agent functionality."""
    with patch('main.ChatOpenAI') as mock_chat:
        mock_instance = Mock()
        mock_chat.return_value = mock_instance
        
        # Mock the bind_tools method
        mock_instance.bind_tools.return_value = mock_instance
        
        # Mock the invoke method to return a mock message
        mock_message = Mock()
        mock_message.content = "Test response"
        mock_message.tool_calls = []
        mock_instance.invoke.return_value = mock_message
        
        yield mock_instance


@pytest.fixture
def mock_sqlite_saver():
    """Mock SqliteSaver for testing."""
    with patch('main.SqliteSaver') as mock_saver:
        mock_instance = Mock()
        mock_saver.from_conn_string.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_dotenv():
    """Mock dotenv loading for testing."""
    with patch('main.load_dotenv') as mock_load:
        yield mock_load


@pytest.fixture(autouse=True)
def clean_test_files():
    """Automatically clean up any test files created during tests."""
    yield
    # Cleanup any test files that might have been created in the current directory
    test_files = [
        "test_file1.txt",
        "test_file2.txt", 
        "hello.txt",
        "goodbye.txt",
        "config.json"
    ]
    for file_name in test_files:
        file_path = Path(file_name)
        if file_path.exists():
            file_path.unlink()


class MockToolCall:
    """Mock tool call for testing."""
    def __init__(self, name: str, args: dict):
        self.name = name
        self.args = args


class MockMessage:
    """Mock message for testing."""
    def __init__(self, content: str = "", tool_calls: list = None):
        self.content = content
        self.tool_calls = tool_calls or []


@pytest.fixture
def mock_tool_call():
    """Factory fixture for creating mock tool calls."""
    def _create_tool_call(name: str, args: dict):
        return MockToolCall(name, args)
    return _create_tool_call


@pytest.fixture
def mock_message():
    """Factory fixture for creating mock messages."""
    def _create_message(content: str = "", tool_calls: list = None):
        return MockMessage(content, tool_calls)
    return _create_message