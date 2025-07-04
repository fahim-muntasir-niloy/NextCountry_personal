# stdio transport

import os
from dotenv import load_dotenv

load_dotenv()
from fastmcp import FastMCP
from langchain_postgres import PGVector
from langchain_ollama import OllamaEmbeddings

mcp = FastMCP("NC_Chatbot_Server")

embedding_engine = OllamaEmbeddings(
    base_url="http://54.80.168.47:11434",
    model="bge-m3:latest",
)
SUPABASE_PG_CONN_URI = os.getenv("SUPABASE_PG_CONN_URI")


@mcp.tool()
def knowledgebase(messages: str, user_id: str):
    """
    keyword: /kb
    Retrieve the query information from knowledgebase stored in postgres database.
    This tool will be used if user only asks to get information from the knowledgebase.

    Args:
        messages (str): The query message.
    Returns:
        list: A list of documents' contents.
    """

    vector_store = PGVector(
        embeddings=embedding_engine,
        collection_name=user_id,
        connection=SUPABASE_PG_CONN_URI,
        use_jsonb=True,
    )

    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"score_threshold": 0.3, "k": 10},
    )
    docs = retriever.invoke(messages)

    return [doc.page_content for doc in docs]


if __name__ == "__main__":
    mcp.run(transport="stdio")
