import warnings
warnings.filterwarnings("ignore")
import os
from dotenv import load_dotenv
load_dotenv()

ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")

from langchain_astradb import AstraDBVectorStore
from langchain_core.tools import tool
from langchain_google_genai import GoogleGenerativeAIEmbeddings

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

from exa_py import Exa
from tavily import TavilyClient
from firecrawl import FirecrawlApp

  
# === Exa ===
exa_client = Exa(api_key=os.environ["EXA_API_KEY"])
@tool
def search_exa(query: str) -> str:
  """Search for webpages based on the 
  query and retrieve their contents."""
  return exa_client.search_and_contents(query,
                                       num_results = 5,
                                       filter_empty_results=True,
                                       livecrawl="auto",
                                       text = True)

# === Tavily ===
tavily_client = TavilyClient(os.environ["TAVILY_API_KEY"])

# def search_tavily(query: str) -> str:
#   """Search for webpages based on the query and 
#   retrieve their contents using tavily."""
#   return tavily_client.search(query,
#                               max_results=5,
#                               include_answer="basic",
#                               )
@tool
def search_tavily(query: str):
  """
  This function fetches context on the query using tavily.
  It will be the default search tool if the user does not specify a tool.
  """
  context = tavily_client.get_search_context(query)

  return context

# === Firecrawler Tool ===
firecrawl_app = FirecrawlApp(api_key=os.getenv("FIRECRAWLER_API_KEY"))

@tool()
def scrape_website(query):
    """
    Used to perform web searches and optionally retrieve content from the results.
    This tool is used to scrape websites for information related to the query.
    """
    try:
      result = firecrawl_app.search(
        query,
        limit=5,
      )
      
      return result
    except Exception as e:
      print(f"Error searching {query}: {e}")
      return None





google_embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
)

@tool
def vecdb_tool(query:str):
  """
  Look into the vector database and retrieve relevant information.
  This is the primary tool used by the agent.
  You must provide the country name in full form and all capital letters.
  example: 'UNITED STATES OF AMERICA'
  """
  
  vector_store = AstraDBVectorStore(
    embedding = google_embedding_model,
    collection_name="visa_details",
    api_endpoint=ASTRA_DB_API_ENDPOINT,
    token=ASTRA_DB_APPLICATION_TOKEN,
    autodetect_collection=True,
    )
  
  retriever = vector_store.as_retriever(
    search_type="similarity", 
    search_kwargs={"k":5, 
                #    "filter": {"country": country}
                   }
  )
  return retriever.invoke(query)


TOOLS = [vecdb_tool, search_exa, search_tavily, scrape_website]