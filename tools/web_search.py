# tools/web_search.py
from langchain_community.tools import DuckDuckGoSearchRun

def get_web_search_tool():
    """Initializes and returns the DuckDuckGo search tool."""
    return DuckDuckGoSearchRun()