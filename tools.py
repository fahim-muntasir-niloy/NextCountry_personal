from langchain_core.tools import tool
import os
from exa_py import Exa
from tavily import TavilyClient

    

# === Exa ===
exa_client = Exa(api_key=os.environ["EXA_API_KEY"])
@tool
def search_exa(query: str) -> str:
  """Search for webpages based on the 
  query and retrieve their contents."""
  return exa_client.search_and_contents(query,
                                       num_results = 5,
                                       filter_empty_results=True,
                                       livecrawl=True,
                                       text = True)

# === Tavily ===
tavily_client = TavilyClient(os.environ["TAVILY_API_KEY"])
@tool
def search_tavily(query: str) -> str:
  """Search for webpages based on the query and 
  retrieve their contents using tavily."""
  return tavily_client.search(query,
                              max_results=5,
                              include_answer="basic",
                              )