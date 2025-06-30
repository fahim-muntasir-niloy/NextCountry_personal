# stdio transport

import os
from dotenv import load_dotenv
load_dotenv()
from fastmcp import FastMCP
from langchain_postgres import PGVector
from langchain_google_genai import GoogleGenerativeAIEmbeddings

mcp = FastMCP("NC_Chatbot_Server")

PGHOST=os.getenv("PGHOST")
PGDATABASE=os.getenv("PGDATABASE")
PGUSER=os.getenv("PGUSER")
PGPASSWORD=os.getenv("PGPASSWORD")


@mcp.tool()
def knowledgebase(messages: str, user_id:str):
    """
    keyword: /kb
    Retrieve the query information from knowledgebase stored in postgres database.
    This tool will be used if user only asks to get information from the knowledgebase.
    
    Args:
        messages (str): The query message.
    Returns:
        list: A list of documents' contents.
    """

    PGVECTOR_CONNECTION_STRING = f"postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}/{PGDATABASE}?sslmode=require&channel_binding=require"

    embedding_engine = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
)

    vector_store = PGVector(
        embeddings=embedding_engine,
        collection_name=user_id,
        connection=PGVECTOR_CONNECTION_STRING,
        use_jsonb=True,
    )


    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={'score_threshold': 0.3,
                       "k":10}
    )
    docs = retriever.invoke(messages)
    
    return [doc.page_content for doc in docs]

   
if __name__ == "__main__":
    mcp.run(transport="stdio")