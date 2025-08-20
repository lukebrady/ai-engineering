from tools import tools, get_tools
from utils import get_env

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv(dotenv_path=".env.secure", override=True)


# LangSmith
LANGSMITH_API_KEY = get_env("LANGSMITH_API_KEY")
LANGSMITH_TRACING_V2 = get_env("LANGSMITH_TRACING_V2")
LANGSMITH_PROJECT = get_env("LANGSMITH_PROJECT")

# OpenAI
OPENAI_API_KEY = get_env("OPENAI_API_KEY")

# Tavily
TAVILY_API_KEY = get_env("TAVILY_API_KEY")


def main():
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        api_key=OPENAI_API_KEY,
    )

    messages = [
        HumanMessage(
            content="Who are some really standout players in the 2025-2026 NFL season?"
        )
    ]
    llm_with_tools = llm.bind_tools(get_tools(), tool_choice="required")
    ai_message = llm_with_tools.invoke(messages)

    for tool_call in ai_message.tool_calls:
        selected_tool = tools[tool_call["name"].lower()]
        tool_result = selected_tool.invoke(tool_call)
        messages.append(tool_result)

    final_response = llm_with_tools.invoke(messages)
    print(final_response.content)


if __name__ == "__main__":
    main()
