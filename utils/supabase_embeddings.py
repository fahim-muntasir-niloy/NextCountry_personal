import os
import sys
sys.path.append("D:\\NextCountry_personal")


from dotenv import load_dotenv
load_dotenv()

SUPABASE_PG_CONN_URI = os.getenv("SUPABASE_PG_CONN_URI")

from langchain_ollama import OllamaEmbeddings
from langchain.text_splitter import MarkdownTextSplitter
from langchain_postgres import PGVector
from langchain.schema import Document

from db.supabase_operations import supabase, list_files

embedding_engine = OllamaEmbeddings(
    base_url="http://54.80.168.47:11434",
    model="bge-m3:latest",
)


def create_embedding_supabase(bucket_id:str):

    latest_file = list_files(bucket_id)[-1]
    file_name = latest_file["name"]

    # Download the file in memory
    file_bytes = supabase.storage.from_(bucket_id).download(file_name)

    # Decode to string (assuming it's a markdown text file)
    markdown_text = file_bytes.decode("utf-8")

    # Create a Document object
    markdown_docs = [Document(page_content=markdown_text, metadata={"file_name": file_name})]

    splitter = MarkdownTextSplitter(chunk_size=800, 
                                    chunk_overlap=200)
    
    split_docs = splitter.split_documents(markdown_docs)


    print(f"Loaded and split {len(markdown_docs)} markdown files into {len(split_docs)} chunks.")

    vector_store = PGVector(
                embeddings=embedding_engine,
                collection_name=bucket_id,
                connection=SUPABASE_PG_CONN_URI,
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

    return {
        "success": True if successful_chunks>0 else False,
        "total_files":len(markdown_docs),        
        "message": f"Document added to PGVector collection: {bucket_id}, {len(failed_chunks)} chunks failed"
    }