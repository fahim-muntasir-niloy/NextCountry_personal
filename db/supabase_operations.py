import os
from dotenv import load_dotenv
load_dotenv()

import uuid
from supabase import create_client, Client


# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase:Client = create_client(SUPABASE_URL, SUPABASE_KEY)



# check if bucket exists
def bucket_exists(bucket_name: str) -> bool:
    # Get list of all buckets
    buckets = supabase.storage.list_buckets()
    return any(bucket.name == bucket_name for bucket in buckets)

# create bucket
def create_bucket(bucket_name: str):
    res = supabase.storage.create_bucket(bucket_name)
    print(f"Bucket created: {bucket_name}")
    return res


def upload_md_file_to_bucket(bucket_name: str, markdown_content, filename: str):
    # Ensure bucket exists
    if not bucket_exists(bucket_name):
        create_bucket(bucket_name)

    # Join list of strings into one markdown string
    if isinstance(markdown_content, list):
        markdown_content = "\n\n".join(markdown_content)

    markdown_bytes = markdown_content.encode('utf-8')

    # Upload with upsert=True to overwrite if needed
    result = supabase.storage.from_(bucket_name).upload(
        path=filename,
        file=markdown_bytes
    )

    if result:
        return f"File uploaded to bucket: {bucket_name}"
    else:
        return "File upload operation failed"


# upload file
def upload_file(bucket_name: str, file_path: str, file_name: str):
    with open(file_path, "rb") as f:
        res = supabase.storage.from_(bucket_name).upload(file_name, f)
        print(res)


# list files
def list_files(bucket_name: str):
    res = supabase.storage.from_(bucket_name).list()
    # print(res)
    return res

# delete file
def delete_file(bucket_name: str, file_name: str):
    res = supabase.storage.from_(bucket_name).remove([file_name])
    print(res)


# bucket_exists("ab7a68c8-d9b2-4c4d-b7ef-445829587759") #-> ab7a68c8-d9b2-4c4d-b7ef-445829587759