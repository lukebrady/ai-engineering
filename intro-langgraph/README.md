# LangGraph Agent with File Operations and Web Search

This project demonstrates a comprehensive LangGraph agent implementation with multiple tool capabilities including web search, file operations (CRUD), and file diffing.

## Features

### 🔍 Web Search
- Search the web for current information using Tavily API
- Automatically triggered when information is not available in the model's knowledge base

### 📁 File Operations (CRUD)
- **Create**: Create new files with specified content
- **Read**: Read and display file contents
- **Update**: Modify existing files with new content
- **Delete**: Remove files from the filesystem

### 🔄 File Diffing
- Compare two files and show unified diff output
- Configurable context lines for better readability
- Handles various file formats and encodings

### 🧠 LangGraph Workflow
- State-based conversation management
- Memory persistence using SQLite
- Proper tool calling and response handling
- Error handling and validation

## Installation

1. Install dependencies using uv:
```bash
uv sync
```

2. Create a `.env.secure` file with your API keys:
```
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_TRACING_V2=true
LANGSMITH_PROJECT=intro-langgraph
```

## Usage

### Running the Examples

```bash
python main.py
```

This will run through several examples demonstrating all the agent's capabilities:
1. Creating a file
2. Reading file contents
3. Updating a file
4. Creating another file
5. Comparing files with diff
6. Web searching for current information

### Using Individual Tools

The agent can handle natural language requests for any of its tools:

#### File Operations
```python
# Create a file
"Create a file called 'config.json' with some sample configuration"

# Read a file
"Show me the contents of config.json"

# Update a file
"Update config.json to include a new setting for debug mode"

# Delete a file
"Delete the config.json file"
```

#### File Diffing
```python
# Compare two files
"Show me the differences between version1.py and version2.py"

# Compare with custom context
"Compare file1.txt and file2.txt with 5 lines of context"
```

#### Web Search
```python
# Search for current information
"What are the latest developments in AI agents?"

# Search for specific topics
"Find information about LangGraph best practices"
```

## Architecture

### Agent State
The agent uses a TypedDict to manage conversation state:
```python
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
```

### Workflow Structure
```
START → agent → [tools] → agent → END
              ↘       ↗
```

- **Agent Node**: Processes user input and decides whether to use tools
- **Tools Node**: Executes the selected tools and returns results
- **Conditional Logic**: Determines whether to continue with tools or end

### Available Tools

1. **web_search**: Search the web using Tavily API
2. **create_file**: Create new files with content validation
3. **read_file**: Read existing files with error handling
4. **update_file**: Update existing files safely
5. **delete_file**: Delete files with confirmation
6. **diff_files**: Compare files and show differences

## Error Handling

The agent includes comprehensive error handling for:
- File not found errors
- Permission issues
- Invalid file paths
- Network connectivity issues
- API rate limits

## Memory and Persistence

- Uses SQLite for conversation memory
- Each conversation thread maintains its own context
- Tool results are preserved across interactions

## Customization

### Adding New Tools
1. Define a new tool function in `tools.py`
2. Create a corresponding Pydantic model for parameters
3. Add the tool to the `tools` dictionary
4. The agent will automatically discover and use the new tool

### Modifying the Agent Behavior
- Update the system message in `create_agent()` function
- Modify the conditional logic in `should_continue()` function
- Adjust the workflow structure as needed

## Dependencies

- **langchain-core**: Core LangChain functionality
- **langchain-openai**: OpenAI integration
- **langchain-tavily**: Tavily search integration
- **langgraph**: Graph-based agent framework
- **langgraph-checkpoint-sqlite**: SQLite memory backend
- **pydantic**: Data validation and settings management

## Examples Output

When you run the agent, you'll see output like:

```
LangGraph Agent with File Operations and Web Search
============================================================

Example 1:
------------------------------
User: Create a file called 'hello.txt' with the content 'Hello, World!'
==================================================
Assistant is calling tools: ['create_file']
Tool (create_file): Successfully created file: hello.txt
Assistant: I've successfully created the file 'hello.txt' with the content 'Hello, World!'.
```

## Contributing

Feel free to extend this agent with additional tools and capabilities. The modular design makes it easy to add new functionality while maintaining the existing workflow structure.