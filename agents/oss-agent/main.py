#!/usr/bin/env python3
"""
OSS Agent Example - A Simple Agent Using Open Source Models

This example demonstrates how to:
1. Connect to a hosted OSS model using OpenAI-compatible API
2. Create function calling tools for the agent to use
3. Implement a basic agent conversation loop with tool execution
4. Handle tool call responses and continue conversations

Prerequisites:
- A running vLLM server with OpenAI API compatibility enabled
- The server should be running on <API_ENDPOINT>:8000/v1 (vLLM default)
- Environment variable API_ENDPOINT should be set to the server's hostname/IP
- Note: For Ollama, change base_url to f"http://{os.getenv('API_ENDPOINT')}:11434" (no /v1)

Usage:
    python main.py
"""

import os
import json
import wikipedia

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

# Load environment variables from a secure .env file
# This keeps sensitive configuration like API endpoints separate from code
load_dotenv(dotenv_path=".env.secure")

# Create OpenAI client configured for vLLM server
# The empty api_key works for most local deployments that don't require auth
# base_url uses vLLM's default port 8000 with /v1 OpenAI-compatible endpoint
client = OpenAI(api_key="", base_url=f"http://{os.getenv('API_ENDPOINT')}:8000/v1")

# Specify the model name - this should match what's loaded in your model server
model = "Qwen/Qwen3-0.6B"


# Define the input schema for our tool using Pydantic
# This ensures type safety and automatic JSON schema generation
class SearchQuery(BaseModel):
    """Input schema for Wikipedia search queries."""
    query: str  # The search term to look up on Wikipedia


# Tool function that the agent can call
# Takes structured input (SearchQuery) and returns results
def wikipedia_search(query: SearchQuery) -> str:
    """
    Search Wikipedia for articles matching the query.
    
    Args:
        query: SearchQuery object containing the search term
        
    Returns:
        List of Wikipedia article titles matching the search
    """
    # Use the wikipedia library to search for articles
    # Returns a list of article titles that match the query
    return wikipedia.search(query)


# Generate JSON schema from our Pydantic model
# This tells the model what parameters the function expects
wikipedia_search_schema = SearchQuery.model_json_schema()

# Define the tool in OpenAI's function calling format
# This is how we tell the model about available functions
tool_definitions = {
    "type": "function",
    "function": {
        "name": "wikipedia_search",  # Function name the model will call
        "description": "Search Wikipedia for information",  # What the function does
        "parameters": wikipedia_search_schema,  # Expected input format
    },
}

# Map function names to actual Python functions
# This allows us to dynamically call the right function based on the model's choice
tools_map = {"wikipedia_search": wikipedia_search}


def main():
    """
    Main function demonstrating the agent conversation loop.
    
    This shows the typical pattern for function-calling agents:
    1. Send initial message with available tools
    2. Handle any tool calls the model makes
    3. Send tool results back to get final response
    """
    # Initialize the conversation with system and user messages
    # The system message sets the agent's behavior and personality
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"},
    ]
    
    # Make the first API call with tools available
    # tool_choice="required" forces the model to use a tool (good for testing)
    # In production, you might use "auto" to let the model decide
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=[tool_definitions],  # List of available tools
        tool_choice="required",    # Force tool usage (optional)
    )
    
    # Add the model's response to our message history
    # This preserves the conversation context for future calls
    messages.append(response.choices[0].message)

    # Check if the model wants to call any tools
    # The model can request multiple tool calls in a single response
    if response.choices[0].message.tool_calls:
        # Process each tool call the model requested
        for tool_call in response.choices[0].message.tool_calls:
            function_name = tool_call.function.name
            
            # Validate that we have the requested function available
            # This prevents errors if the model hallucinates function names
            if function_name not in tools_map:
                # Return an error message to the model if function doesn't exist
                messages.append(
                    {
                        "role": "tool",
                        "content": json.dumps(
                            {"error": f"Function {function_name} not found"}
                        ),
                        "tool_call_id": tool_call.id,  # Must match the call ID
                    }
                )
                continue
            
            # Parse the function arguments from JSON
            # The model provides arguments as a JSON string
            function_args = json.loads(tool_call.function.arguments)

            # Execute the actual function with the provided arguments
            # This is where the real work happens - calling external APIs, databases, etc.
            result = tools_map[function_name](**function_args)

            # Send the function result back to the model
            # The model will use this information to generate its final response
            messages.append(
                {
                    "role": "tool",  # Special role for tool results
                    "content": json.dumps(result),  # Function output as JSON
                    "tool_call_id": tool_call.id,   # Must match the original call ID
                }
            )

    # Make a final API call to get the model's response using the tool results
    # No tools are needed this time - we just want the final answer
    final_response = client.chat.completions.create(
        model=model,
        messages=messages,  # Includes original query + tool calls + tool results
    )
    
    # Print the model's final response
    # This should incorporate the information gathered from the tool calls
    print(final_response.choices[0].message.content)


if __name__ == "__main__":
    # Example of how to extend this agent:
    # 1. Add more tools by creating new functions and adding them to tools_map
    # 2. Use different models by changing the 'model' variable
    # 3. Create interactive loops by wrapping main() in a while loop
    # 4. Add memory/context persistence by storing messages between runs
    # 5. Add error handling and retry logic for robustness
    
    main()
