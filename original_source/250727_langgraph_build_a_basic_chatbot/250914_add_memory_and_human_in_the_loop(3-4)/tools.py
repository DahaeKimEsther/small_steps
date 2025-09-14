from langchain_tavily import TavilySearch
from langgraph.types import interrupt
from langchain_core.tools import tool

tavily_search = TavilySearch(max_results=2)
# tool.invoke("What's a 'node' in Langgraph?")

@tool
def human_assistance(query:str) -> str:
    """Request assistance from a human"""
    human_response = interrupt({"query": query})
    return human_response["data"]

tools = [tavily_search, human_assistance]
