import os
from dotenv import load_dotenv
load_dotenv()

from appwrite.client import Client
from appwrite.input_file import InputFile
from appwrite.services.storage import Storage       # blob storage

client = Client()

client.set_endpoint('https://nyc.cloud.appwrite.io/v1')  # Replace with your Appwrite endpoint
client.set_project('686042880022242d7e19')       # Replace with your project ID
client.set_key(os.getenv("APPWRITE_API_KEY"))              # Replace with your API key



storage = Storage(client)

file_path = '/home/fahim-muntasir/Office/NextCountry_personal/responses/report_27_06_2025_01_06_20.md'

result = storage.create_file(
    bucket_id='68604314000b649ca2c5',
    file_id='unique()',
    file=InputFile.from_path(file_path)
)

print(result)