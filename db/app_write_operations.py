import os
from dotenv import load_dotenv
load_dotenv()

import uuid
from appwrite.client import Client
from appwrite.input_file import InputFile
from appwrite.services.storage import Storage       # blob storage

client = Client()

client.set_endpoint("https://nyc.cloud.appwrite.io/v1")  # Replace with your Appwrite endpoint
client.set_project(os.getenv("APPWRITE_PROJECT_ID"))       # Replace with your project ID
client.set_key(os.getenv("APPWRITE_API_KEY"))              # Replace with your API key

storage_client = Storage(client)

# Bucket CRUD Operation -> current user id: 2db51638-5ca2-4661-8705-7a253ce21e8c

def create_bucket(user_id:str, user_name: str):
    result = storage_client.create_bucket(
        bucket_id=user_id,
        name=user_name,
        file_security=True,               # True = enable file-level permission control
        enabled=True                      # Whether the bucket is active
    )

    return result

def delete_bucket(user_id:str):
    result = storage_client.delete_bucket(
        bucket_id = user_id
    )

    if result:
        return f"Deleted bucket {user_id}"
    else:
        return "Delete operation failed"


# File CRUD
def upload_file_to_bucket(user_id: str, markdown_content, filename: str):
    # Join list of strings into one markdown string
    if isinstance(markdown_content, list):
        markdown_content = "\n\n".join(markdown_content)

    markdown_bytes = markdown_content.encode('utf-8')
    in_memory_file = InputFile.from_bytes(markdown_bytes, filename=filename)

    result = storage_client.create_file(
        bucket_id=user_id,
        file_id=str(uuid.uuid4()),
        file=in_memory_file
    )

    if result:
        return f"File uploaded to bucket: {user_id}"
    else:
        return "File upload operation failed"
