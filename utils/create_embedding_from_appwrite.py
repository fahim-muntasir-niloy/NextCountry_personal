import re
import os
from dotenv import load_dotenv
load_dotenv()

import io
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.schema import Document
from langchain.text_splitter import MarkdownTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector

from appwrite.client import Client
from appwrite.services.storage import Storage


# --- Neon DB Setup  ---
PGHOST=os.getenv("PGHOST")
PGDATABASE=os.getenv("PGDATABASE")
PGUSER=os.getenv("PGUSER")
PGPASSWORD=os.getenv("PGPASSWORD")

# --- Appwrite Setup ---
client = Client()

client.set_endpoint('https://nyc.cloud.appwrite.io/v1')
client.set_project(os.getenv("APPWRITE_PROJECT_ID"))
client.set_key(os.getenv("APPWRITE_API_KEY")) 
storage = Storage(client)


# --- Markdown Loader ---
def load_markdown_from_appwrite(bucket_id: str, file_id: str, file_name: str) -> Document:
    file_bytes = storage.get_file_download(bucket_id=bucket_id, file_id=file_id)
    text = file_bytes.decode("utf-8")  # decode Markdown text
    return Document(page_content=text, metadata={"file_id": file_id, "filename": file_name})


def load_latest_markdown_from_appwrite(bucket_id: str) -> Document:
    # Step 1: Get the list of files (most recent is first)
    files = storage.list_files(bucket_id=bucket_id)
    if not files["files"]:
        raise ValueError("No files found in the bucket.")
    
    latest_file = files["files"][-1]  # Pick the most recent file
    file_id = latest_file["$id"]
    file_name = latest_file["name"]
    
    # Step 2: Download the file content
    file_bytes = storage.get_file_download(bucket_id=bucket_id, file_id=file_id)
    text = file_bytes.decode("utf-8")

    return Document(page_content=text, metadata={"file_id": file_id, "filename": file_name})


# print([load_latest_markdown_from_appwrite("2db51638-5ca2-4661-8705-7a253ce21e8c")])

def create_embedding(bucket_id:str):

    # # --- Load All .md Files from Bucket ---
    # files = storage.list_files(bucket_id=bucket_id)["files"]

    # markdown_docs = []
    # for file in files:
    #     if file["name"].endswith(".md"):
    #         # doc = load_markdown_from_appwrite(bucket_id, file["$id"], file["name"])
    #         doc = load_latest_markdown_from_appwrite(bucket_id)
    #         markdown_docs.append(doc)

    markdown_docs = [load_latest_markdown_from_appwrite(bucket_id)]

    # --- Chunking ---
    splitter = MarkdownTextSplitter(chunk_size=500, 
                                    chunk_overlap=30)
    
    split_docs = splitter.split_documents(markdown_docs)


    print(f"Loaded and split {len(markdown_docs)} markdown files into {len(split_docs)} chunks.")

    # --- embedding ---
    embedding_engine = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
    )

    PGVECTOR_CONNECTION_STRING = f"postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}/{PGDATABASE}?sslmode=require&channel_binding=require"

    vector_store = PGVector(
                embeddings=embedding_engine,
                collection_name=bucket_id,
                connection=PGVECTOR_CONNECTION_STRING,
                use_jsonb=True,
            )
    
    
    successful_chunks = 0
    failed_chunks = []

    for i, split in enumerate(split_docs):
        try:
            vector_store.add_documents([split])
            successful_chunks += 1
        except Exception as e:
            failed_chunks.append({
                "index": i,
                "error": str(e),
                "content_preview": split.page_content[:100]  # Optional: for debug
            })
        except Exception as e:
            return {
                "success": False,
                "message": f"Error adding document to PGVector: {e}",
            }

    return {
        "success": True if successful_chunks>0 else False,
        "total_files":len(markdown_docs),        
        "message": f"Document added to PGVector collection: {bucket_id}, {len(failed_chunks)} chunks failed"
    }