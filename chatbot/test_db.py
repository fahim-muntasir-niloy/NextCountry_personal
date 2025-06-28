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

client.set_endpoint('https://nyc.cloud.appwrite.io/v1')  # Replace with your Appwrite endpoint
client.set_project('686042880022242d7e19')       # Replace with your project ID
client.set_key(os.getenv("APPWRITE_API_KEY"))              # Replace with your API key
client.set_session('')
storage = Storage(client)


# --- Markdown Loader ---
def load_markdown_from_appwrite(bucket_id: str, file_id: str, file_name: str) -> Document:
    file_bytes = storage.get_file_download(bucket_id=bucket_id, file_id=file_id)
    text = file_bytes.decode("utf-8")  # decode Markdown text
    return Document(page_content=text, metadata={"file_id": file_id, "filename": file_name})

# --- Load All .md Files from Bucket ---
bucket_id = "68604314000b649ca2c5"
files = storage.list_files(bucket_id=bucket_id)["files"]

markdown_docs = []
for file in files:
    if file["name"].endswith(".md"):
        doc = load_markdown_from_appwrite(bucket_id, file["$id"], file["name"])
        markdown_docs.append(doc)

# --- Optional Chunking ---
splitter = MarkdownTextSplitter(chunk_size=500, chunk_overlap=50)
split_docs = splitter.split_documents(markdown_docs)

# Now you can use split_docs in your RAG pipeline or vector store
print(f"Loaded and split {len(markdown_docs)} markdown files into {len(split_docs)} chunks.")

# --- embedding ---
embedding_engine = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
)

PGVECTOR_CONNECTION_STRING = f"postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}/{PGDATABASE}?sslmode=require&channel_binding=require"

vector_store = PGVector(
            embeddings=embedding_engine,
            collection_name="test_vectors",
            connection=PGVECTOR_CONNECTION_STRING,
            use_jsonb=True,
        )

vector_store.add_documents(split_docs)

print("done")