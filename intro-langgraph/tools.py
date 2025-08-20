from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain_tavily import TavilySearch

from utils import get_env

class SearchRequest(BaseModel):
    query: str = Field(description="The query to search for")

@tool
def web_search(request: SearchRequest):
    """
    Search the web for information if you determine that the user's query is not in your knowledge base.
    """
    print(f"Searching for {request.query}")
    search = TavilySearch(max_results=2)
    search_docs = search.invoke(request.query)
    return search_docs

# Tools to be used by LangChain
tools = {
    "web_search": web_search
}

def get_tools():
    return list(tools.values())

if __name__ == "__main__":
    print(get_tools())