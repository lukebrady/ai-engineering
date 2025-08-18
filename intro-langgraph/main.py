import os
import json

from tools import tools, tool_definitions

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_tavily import TavilySearch

load_dotenv(dotenv_path=".env.secure", override=True)


def _get_env(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise ValueError(f"Environment variable {key} is not set")
    return value


# LangSmith
LANGSMITH_API_KEY = _get_env("LANGSMITH_API_KEY")
LANGSMITH_TRACING_V2 = _get_env("LANGSMITH_TRACING_V2")
LANGSMITH_PROJECT = _get_env("LANGSMITH_PROJECT")

# OpenAI
OPENAI_API_KEY = _get_env("OPENAI_API_KEY")

# Tavily
TAVILY_API_KEY = _get_env("TAVILY_API_KEY")


def main():
    llm = ChatOpenAI(
        model="gpt-5-nano-2025-08-07",
        temperature=0,
        api_key=OPENAI_API_KEY,
    )

    messages = [HumanMessage(content="Who are some really standout players in the 2025-2026 NFL season?")]
    llm_with_tools = llm.bind_tools(tools, tool_choice="required")
    response = llm_with_tools.invoke(messages)
    print(response.tool_calls)


if __name__ == "__main__":
    main()
