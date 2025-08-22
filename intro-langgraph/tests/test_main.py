"""Simplified integration tests for main.py agent workflow."""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path

# Import main module components
from main import AgentState, run_agent_conversation, main


class TestAgentState:
    """Test cases for AgentState TypedDict."""
    
    def test_agent_state_structure(self):
        """Test that AgentState has correct structure."""
        from langchain_core.messages import HumanMessage
        
        # Create a sample state
        state: AgentState = {
            "messages": [HumanMessage(content="test message")]
        }
        
        assert "messages" in state
        assert len(state["messages"]) == 1
        assert state["messages"][0].content == "test message"


class TestRunAgentConversation:
    """Test cases for run_agent_conversation function."""
    
    @patch('main.create_agent')
    @patch('builtins.print')
    def test_run_agent_conversation_basic(self, mock_print, mock_create_agent):
        """Test basic agent conversation flow."""
        # Create a mock agent
        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent
        
        # Mock the stream method to return some events
        mock_message = Mock()
        mock_message.content = "Test response"
        mock_message.tool_calls = []
        
        mock_events = [
            {"messages": [mock_message]},
        ]
        mock_agent.stream.return_value = mock_events
        
        # Run the conversation
        run_agent_conversation("test query", "test_thread")
        
        # Verify agent was created and called
        mock_create_agent.assert_called_once()
        mock_agent.stream.assert_called_once()
        
        # Verify the call arguments
        call_args = mock_agent.stream.call_args
        initial_state, config = call_args[0]
        
        assert "messages" in initial_state
        assert len(initial_state["messages"]) == 1
        assert initial_state["messages"][0].content == "test query"
        assert config["configurable"]["thread_id"] == "test_thread"


class TestMainFunction:
    """Test cases for main function."""
    
    @patch('main.run_agent_conversation')
    @patch('builtins.print')
    def test_main_function_runs_examples(self, mock_print, mock_run_conversation):
        """Test that main function runs all example conversations."""
        main()
        
        # Verify that run_agent_conversation was called multiple times
        assert mock_run_conversation.call_count == 6
        
        # Verify the example queries were used
        call_args_list = mock_run_conversation.call_args_list
        queries = [call[0][0] for call in call_args_list]
        
        expected_queries = [
            "Create a file called 'hello.txt' with the content 'Hello, World!'",
            "Read the content of hello.txt",
            "Update hello.txt to say 'Hello, LangGraph!'",
            "Create another file called 'goodbye.txt' with 'Goodbye, World!'",
            "Show me the differences between hello.txt and goodbye.txt",
            "Search for information about the latest developments in AI agents",
        ]
        
        assert queries == expected_queries


class TestAgentMemoryAndState:
    """Test cases for agent memory and state management."""
    
    @patch('main.create_agent')
    @patch('builtins.print')
    def test_different_thread_ids_create_separate_conversations(
        self, 
        mock_print, 
        mock_create_agent
    ):
        """Test that different thread IDs create separate conversation contexts."""
        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent
        
        mock_message = Mock()
        mock_message.content = "response"
        mock_message.tool_calls = []
        
        mock_agent.stream.return_value = [{"messages": [mock_message]}]
        
        # Run conversations with different thread IDs
        run_agent_conversation("query 1", "thread_1")
        run_agent_conversation("query 2", "thread_2")
        
        # Verify both calls were made with different configurations
        assert mock_agent.stream.call_count == 2
        
        call_configs = [call[0][1] for call in mock_agent.stream.call_args_list]
        assert call_configs[0]["configurable"]["thread_id"] == "thread_1"
        assert call_configs[1]["configurable"]["thread_id"] == "thread_2"
    
    @patch('main.create_agent')
    @patch('builtins.print')
    def test_same_thread_id_maintains_conversation_context(
        self, 
        mock_print, 
        mock_create_agent
    ):
        """Test that same thread ID maintains conversation context."""
        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent
        
        mock_message = Mock()
        mock_message.content = "response"
        mock_message.tool_calls = []
        
        mock_agent.stream.return_value = [{"messages": [mock_message]}]
        
        # Run multiple conversations with same thread ID
        run_agent_conversation("query 1", "same_thread")
        run_agent_conversation("query 2", "same_thread")
        
        # Verify both calls used the same thread configuration
        call_configs = [call[0][1] for call in mock_agent.stream.call_args_list]
        assert call_configs[0]["configurable"]["thread_id"] == "same_thread"
        assert call_configs[1]["configurable"]["thread_id"] == "same_thread"


class TestAgentErrorHandling:
    """Test cases for agent error handling scenarios."""
    
    @patch('main.create_agent')
    @patch('builtins.print')
    def test_conversation_handles_agent_creation_failure(self, mock_print, mock_create_agent):
        """Test conversation handling when agent creation fails."""
        mock_create_agent.side_effect = Exception("Agent creation failed")
        
        with pytest.raises(Exception, match="Agent creation failed"):
            run_agent_conversation("test query")
    
    @patch('main.create_agent')
    @patch('builtins.print')
    def test_run_agent_conversation_error_handling(self, mock_print, mock_create_agent):
        """Test agent conversation error handling."""
        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent
        
        # Make the agent raise an exception
        mock_agent.stream.side_effect = Exception("Test error")
        
        # The function should handle the error gracefully
        with pytest.raises(Exception, match="Test error"):
            run_agent_conversation("test query")