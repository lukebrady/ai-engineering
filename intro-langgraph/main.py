import operator
from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, ToolMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.sqlite import SqliteSaver

from tools import tools, get_tools
from utils import get_env

load_dotenv(dotenv_path=".env.secure", override=True)

# Environment variables
LANGSMITH_API_KEY = get_env("LANGSMITH_API_KEY")
LANGSMITH_TRACING_V2 = get_env("LANGSMITH_TRACING_V2")
LANGSMITH_PROJECT = get_env("LANGSMITH_PROJECT")
OPENAI_API_KEY = get_env("OPENAI_API_KEY")
TAVILY_API_KEY = get_env("TAVILY_API_KEY")

class AgentState(TypedDict):
    """State of the agent conversation."""
    messages: Annotated[Sequence[BaseMessage], add_messages]

def create_agent():
    """Create the LangGraph agent with tools."""
    
    # Initialize the LLM with tools
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        api_key=OPENAI_API_KEY,
    )
    
    # Bind tools to the LLM
    llm_with_tools = llm.bind_tools(get_tools())
    
    # System message for the agent
    system_message = SystemMessage(
        content="""You are a helpful AI assistant with access to various tools for file operations and web search.

Available tools:
- web_search: Search the web for current information
- create_file: Create new files with specified content
- read_file: Read the contents of existing files
- update_file: Update existing files with new content
- delete_file: Delete files from the filesystem
- diff_files: Compare two files and show differences

You should:
1. Use web_search when you need current information not in your knowledge base
2. Use file operations to help users manage their files
3. Always provide clear feedback about what operations you performed
4. Handle errors gracefully and provide helpful error messages
5. Use diff_files to show differences between file versions

Be helpful, accurate, and safe in your operations."""
    )
    
    def should_continue(state: AgentState) -> str:
        """Determine if the agent should continue or end."""
        messages = state["messages"]
        last_message = messages[-1]
        
        # If the last message has tool calls, continue to tools
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            return "tools"
        # Otherwise, end the conversation
        return END
    
    def call_model(state: AgentState) -> dict:
        """Call the model with the current state."""
        messages = state["messages"]
        
        # Add system message if it's the first call
        if not any(isinstance(msg, SystemMessage) for msg in messages):
            messages = [system_message] + messages
        
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}
    
    # Create the state graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", ToolNode(get_tools()))
    
    # Add edges
    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            END: END,
        }
    )
    workflow.add_edge("tools", "agent")
    
    # Add memory
    memory = SqliteSaver.from_conn_string(":memory:")
    
    # Compile the graph
    app = workflow.compile(checkpointer=memory)
    
    return app

def run_agent_conversation(query: str, thread_id: str = "1"):
    """Run a conversation with the agent."""
    app = create_agent()
    
    # Create the initial state
    initial_state = {"messages": [HumanMessage(content=query)]}
    
    # Configuration for the conversation
    config = {"configurable": {"thread_id": thread_id}}
    
    print(f"User: {query}")
    print("=" * 50)
    
    # Run the agent
    for event in app.stream(initial_state, config, stream_mode="values"):
        if "messages" in event:
            # Get the last message
            last_message = event["messages"][-1]
            
            # Only print assistant messages (not tool calls or system messages)
            if hasattr(last_message, 'content') and last_message.content:
                if not isinstance(last_message, (SystemMessage, ToolMessage)):
                    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
                        # This is an assistant message with tool calls
                        print(f"Assistant is calling tools: {[tc['name'] for tc in last_message.tool_calls]}")
                    elif hasattr(last_message, 'name'):
                        # This is a tool response
                        print(f"Tool ({last_message.name}): {last_message.content}")
                    else:
                        # This is a regular assistant response
                        print(f"Assistant: {last_message.content}")

def main():
    """Main function with example usage."""
    print("LangGraph Agent with File Operations and Web Search")
    print("=" * 60)
    
    # Example conversations demonstrating different capabilities
    examples = [
        "Create a file called 'hello.txt' with the content 'Hello, World!'",
        "Read the content of hello.txt",
        "Update hello.txt to say 'Hello, LangGraph!'",
        "Create another file called 'goodbye.txt' with 'Goodbye, World!'",
        "Show me the differences between hello.txt and goodbye.txt",
        "Search for information about the latest developments in AI agents",
    ]
    
    for i, query in enumerate(examples, 1):
        print(f"\nExample {i}:")
        print("-" * 30)
        run_agent_conversation(query, thread_id=f"example_{i}")
        print()

if __name__ == "__main__":
    main()
