from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain_tavily import TavilySearch

class SearchRequest(BaseModel):
    query: str = Field(description="The query to search for")

@tool
def search(request: SearchRequest):
    """
    Search the web for information if you determine that the user's query is not in your knowledge base.
    """
    print(f"Searching for {request.query}")
    search = TavilySearch(max_results=2)
    search_docs = search.invoke(request.query)
    return search_docs

# Generate the JSON tool schemas
search_schema = SearchRequest.model_json_schema()

# Define the available tool definitions
tool_definitions = [
    {
        "type": "function",
        "function": {
            "name": "search",
            "description": "Search the web for information",
            "parameters": search_schema,
        },
    }
]

# Tools to be used by LangChain
tools = [search]
