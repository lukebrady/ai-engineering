import os
import json
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
    search = TavilySearch(max_results=2, api_key=TAVILY_API_KEY)
    search_docs = search.invoke("What is the capital of France?")
    json_search_docs = json.dumps(search_docs)
    
    messages = [
        HumanMessage(content=f"Summarize the following search results: {json_search_docs}"),
    ]
    response = llm.invoke(messages)
    print(response.content)


if __name__ == "__main__":
    main()
