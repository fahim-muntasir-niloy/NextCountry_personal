from datetime import datetime
import os
import json
from langchain.tools import tool

# WIP

@tool
def save_report(data=str):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"-----------------------------------\nTimestamp:{time}\n\n{data}\n--------------------------------\n"
    filename=f"report_{time}.txt"
    filename = filename.replace(":", "_")  # Replace ':' with '-' to avoid issues in filenames
    with open(filename, "a", encoding="utf-8") as file:
        file.write(formatted_text)
        
    return f"Report saved as {filename}"
    