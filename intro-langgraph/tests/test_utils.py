"""Unit tests for utils.py module."""

import os
import pytest
from unittest.mock import patch
from utils import get_env


class TestGetEnv:
    """Test cases for get_env function."""
    
    def test_get_env_returns_existing_value(self):
        """Test that get_env returns value when environment variable exists."""
        with patch.dict(os.environ, {"TEST_VAR": "test_value"}):
            result = get_env("TEST_VAR")
            assert result == "test_value"
    
    def test_get_env_raises_error_for_missing_variable(self):
        """Test that get_env raises ValueError when environment variable doesn't exist."""
        # Ensure the variable doesn't exist
        if "NONEXISTENT_VAR" in os.environ:
            del os.environ["NONEXISTENT_VAR"]
        
        with pytest.raises(ValueError, match="Environment variable NONEXISTENT_VAR is not set"):
            get_env("NONEXISTENT_VAR")
    
    def test_get_env_raises_error_for_empty_value(self):
        """Test that get_env raises ValueError when environment variable is empty."""
        with patch.dict(os.environ, {"EMPTY_VAR": ""}):
            with pytest.raises(ValueError, match="Environment variable EMPTY_VAR is not set"):
                get_env("EMPTY_VAR")
    
    def test_get_env_with_whitespace_value(self):
        """Test that get_env returns whitespace values as-is."""
        with patch.dict(os.environ, {"WHITESPACE_VAR": "  test  "}):
            result = get_env("WHITESPACE_VAR")
            assert result == "  test  "
    
    def test_get_env_with_special_characters(self):
        """Test that get_env handles special characters in values."""
        special_value = "test@#$%^&*()_+-={}[]|\\:;\"'<>,.?/"
        with patch.dict(os.environ, {"SPECIAL_VAR": special_value}):
            result = get_env("SPECIAL_VAR")
            assert result == special_value
    
    def test_get_env_with_numeric_value(self):
        """Test that get_env returns numeric values as strings."""
        with patch.dict(os.environ, {"NUMERIC_VAR": "12345"}):
            result = get_env("NUMERIC_VAR")
            assert result == "12345"
            assert isinstance(result, str)
    
    def test_get_env_case_sensitive(self):
        """Test that get_env is case-sensitive for variable names."""
        with patch.dict(os.environ, {"test_var": "lowercase"}):
            # Should not find TEST_VAR (uppercase)
            with pytest.raises(ValueError):
                get_env("TEST_VAR")
            
            # Should find test_var (lowercase)
            result = get_env("test_var")
            assert result == "lowercase"