from tools import get_tools
from utils import get_env

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from typing import Annotated, TypedDict, List
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
import os

load_dotenv(dotenv_path=".env.secure", override=True)


# LangSmith (optional)
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_TRACING_V2 = os.getenv("LANGSMITH_TRACING_V2")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT")

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class AgentState(TypedDict):
    messages: Annotated[List, add_messages]


def build_app():
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        api_key=OPENAI_API_KEY,
    )

    tools = get_tools()
    llm_with_tools = llm.bind_tools(tools)

    def call_model(state: AgentState):
        response = llm_with_tools.invoke(state["messages"])
        return {"messages": [response]}

    graph = StateGraph(AgentState)
    graph.add_node("agent", call_model)
    graph.add_node("tools", ToolNode(tools))
    graph.set_entry_point("agent")
    graph.add_conditional_edges("agent", tools_condition)
    graph.add_edge("tools", "agent")

    return graph.compile()


def main():
    app = build_app()

    # Default demo message exercises file tools (no external API keys required).
    default_messages = [
        SystemMessage(content=(
            "You are a helpful AI assistant. Use tools when beneficial. "
            "Prefer the provided file tools for filesystem tasks within the workspace."
        )),
        HumanMessage(content=(
            "Create a file at /workspace/intro-langgraph/demo.txt with the text 'hello world', "
            "then read it back, then append a new line 'second line', read again, and finish by "
            "showing a diff between /workspace/intro-langgraph/demo.txt and /workspace/intro-langgraph/tools.py."
        )),
    ]

    final_state = app.invoke({"messages": default_messages})
    final_messages = final_state["messages"]
    print(final_messages[-1].content)


if __name__ == "__main__":
    main()
