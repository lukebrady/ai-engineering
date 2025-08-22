# AI Engineering

Learning AI engineering in the open

## Projects

### 🤖 LangGraph Agent with Comprehensive Tool Support

**Location**: `intro-langgraph/`

A sophisticated LangGraph agent implementation featuring:

- **🔍 Web Search**: Real-time web search using Tavily API
- **📁 File Operations**: Complete CRUD operations for file management
  - Create files with content validation
  - Read existing files safely
  - Update files with new content
  - Delete files with confirmation
- **🔄 File Diffing**: Compare files and show unified diff output
- **🧠 LangGraph Workflow**: State-based conversation management with memory persistence
- **🛡️ Error Handling**: Comprehensive validation and error recovery

#### Features

- **Modular Tool Architecture**: Easy to extend with new capabilities
- **Memory Persistence**: SQLite-based conversation history
- **Natural Language Interface**: Handle complex multi-step requests
- **Safe File Operations**: Built-in validation and error handling
- **Configurable Diffing**: Customizable context lines for file comparisons

#### Quick Start

```bash
cd intro-langgraph
uv sync
# Add your API keys to .env.secure
uv run python main.py
```

#### Example Interactions

```python
# File management
"Create a configuration file with database settings"
"Update the config to use a different database host"
"Show me the differences between the old and new config"

# Web search + file operations
"Search for Python best practices and save them to a file"
"Find the latest LangGraph documentation and create a summary"

# Complex workflows
"Compare my current code with the backup version and tell me what changed"
```

See the [intro-langgraph README](intro-langgraph/README.md) for detailed documentation.

---

*This repository documents my journey learning AI engineering concepts, frameworks, and best practices.*
