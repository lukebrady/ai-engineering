import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env.secure"))

from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage, HumanMessage
from langgraph.prebuilt import ToolNode
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from tools import tools

llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-Coder-32B-Instruct",
    huggingfacehub_api_token=os.getenv("HUGGING_FACE_TOKEN"),
)


# Generate the chat interface, including the tools

chat = ChatHuggingFace(llm=llm, verbose=True)
tools = tools
chat_with_tools = chat.bind_tools(tools)


# Generate the AgentState and Agent Graph
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


def assistant(state: AgentState):
    return {
        "messages": [chat_with_tools.invoke(state["messages"])],
    }


# The graph
builder = StateGraph(AgentState)

# Define nodes: these do the work
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

# Define edges: these determine how the control flow moves
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    # If the latest message requires a tool, route to tools
    # Otherwise, provide a direct response
    tools_condition,
)
builder.add_edge("tools", "assistant")
alfred = builder.compile()

response = alfred.invoke({"messages": "Tell me about 'Lady Ada Lovelace'"})

print("🎩 Alfred's Response:")
print(response["messages"][-1].content)

response = alfred.invoke(
    {
        "messages": "What's the weather like in Paris tonight? Will it be suitable for our fireworks display?"
    }
)

print("🎩 Alfred's Response:")
print(response["messages"][-1].content)

response = alfred.invoke(
    {
        "messages": "One of our guests is from Qwen. What can you tell me about their most popular model?"
    }
)

print("🎩 Alfred's Response:")
print(response["messages"][-1].content)

response = alfred.invoke(
    {
        "messages": "I need to speak with 'Dr. Nikola Tesla' about recent advancements in wireless energy. Can you help me prepare for this conversation?"
    }
)

print("🎩 Alfred's Response:")
print(response["messages"][-1].content)

# First interaction
response = alfred.invoke(
    {
        "messages": [
            HumanMessage(
                content="Tell me about 'Lady Ada Lovelace'. What's her background and how is she related to me?"
            )
        ]
    }
)


print("🎩 Alfred's Response:")
print(response["messages"][-1].content)
print()

# Second interaction (referencing the first)
response = alfred.invoke(
    {
        "messages": response["messages"]
        + [HumanMessage(content="What projects is she currently working on?")]
    }
)

print("🎩 Alfred's Response:")
print(response["messages"][-1].content)
