import warnings
warnings.filterwarnings("ignore")
from langchain_core.tools import tool

import os
from dotenv import load_dotenv
load_dotenv()
HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")

from exa_py import Exa
from tavily import TavilyClient
from langchain_astradb import AstraDBVectorStore

    

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
@tool
def search_tavily(query: str) -> str:
  """Search for webpages based on the query and 
  retrieve their contents using tavily."""
  return tavily_client.search(query,
                              max_results=5,
                              include_answer="basic",
                              )


# === retriver tool ===
from langchain_google_genai import GoogleGenerativeAIEmbeddings

google_embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
)
vector_store = AstraDBVectorStore(
    embedding = google_embedding_model,
    collection_name="visa_information_v3",
    api_endpoint=ASTRA_DB_API_ENDPOINT,
    token=ASTRA_DB_APPLICATION_TOKEN,
    autodetect_collection=True,
)

@tool
def vecdb_tool(query:str, country:str):
  """
  Look into the vector database and retrieve relevant information.
  This is the primary tool used by the agent.
  You must provide the country name in full form and all capital letters.
  example: 'UNITED STATES OF AMERICA'
  """
  retriever = vector_store.as_retriever(
    search_type="similarity", 
    search_kwargs={"k":15, 
                   "filter": {"country": country}
                   }
  )
  return retriever.invoke(query)

