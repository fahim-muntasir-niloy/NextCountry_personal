import warnings

warnings.filterwarnings("ignore")
import os
from dotenv import load_dotenv

load_dotenv()

ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")

from langchain_astradb import AstraDBVectorStore
from langchain_core.tools import tool
from tavily import TavilyClient
from firecrawl import FirecrawlApp


# === Tavily ===
tavily_client = TavilyClient(os.environ["TAVILY_API_KEY"])


@tool
def search_tavily(query: str):
    """
    This function fetches context on the query using tavily.
    It will be the default search tool if the user does not specify a tool.
    """
    result = tavily_client.search(
        query,
        auto_parameters=True,
    )

    return result


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


from langchain_ollama import OllamaEmbeddings

embedding_engine = OllamaEmbeddings(
    base_url="http://54.80.168.47:11434",
    model="bge-m3:latest",
)


@tool
def vecdb_tool(query: str):
    """
    Look into the vector database and retrieve relevant information.
    This is the primary tool used by the agent.
    You must provide the country name in full form and all capital letters.
    example: 'UNITED STATES OF AMERICA'
    """

    vector_store = AstraDBVectorStore(
        embedding=embedding_engine,
        collection_name="nc_visa_details_vector_db",
        api_endpoint=ASTRA_DB_API_ENDPOINT,
        token=ASTRA_DB_APPLICATION_TOKEN,
        autodetect_collection=True,
    )

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": 15,
            #    "filter": {"country": country}
        },
    )

    results = retriever.invoke(query)
    # for result in results:
    return [result.page_content for result in results]


TOOLS = [vecdb_tool, search_tavily, scrape_website]
