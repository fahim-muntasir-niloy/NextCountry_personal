from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.messages import AIMessage
import re
import json
from typing import Optional
import uuid

from rich import print

from supervisor_agent.supervisor import next_country_supervisor
from supervisor_agent.output_agent import output_agent
from utils.save_report import save_report

from db.supabase_operations import upload_md_file_to_bucket
from utils.supabase_embeddings import create_embedding_supabase

from datetime import datetime


class NextCountryRequest(BaseModel):
    message: dict
    user_id: Optional[str] = str(uuid.uuid4())

    # "ab7a68c8-d9b2-4c4d-b7ef-445829587759"


app = FastAPI(
    title="Next Country API",
    description="API for the Next Country project",
    version="2.0.0",
    contact={
        "name": "Fahim Muntasir",
        "url": "https://nextcountry.com",
    },
)


@app.post("/next_country")
def json_output_flow(request: NextCountryRequest):
    data = request.message
    user_id = request.user_id
    print(f"Received message:  {data}, user_id: {user_id}")

    # Handling input json -> make it string
    pretty_json_str = json.dumps(data, indent=4)
    escaped_json_str = pretty_json_str.replace("\n", "\\n").replace('"', '\\"')

    supervisor_response = next_country_supervisor.invoke({"messages": escaped_json_str})

    for m in supervisor_response["messages"]:
        m.pretty_print()

    # save_report(supervisor_response)
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    filename = f"{user_id}_{dt_string}.md"

    ai_response = [
        m for m in supervisor_response["messages"] if isinstance(m, AIMessage)
    ]
    pretty_response = [m.content for m in ai_response]

    print(upload_md_file_to_bucket(user_id, pretty_response, filename=filename))

    output_response = output_agent.invoke({"messages": pretty_response})

    output = output_response["messages"][-1].content

    # Handling output string -> convert to json
    json_match = re.search(r"```json\n(.*?)```", output, re.DOTALL)
    if json_match:
        json_str = json_match.group(1)
        clean_json = json.loads(json_str)
        print(clean_json)

        print(create_embedding_supabase(user_id))

        return clean_json

    else:
        return f"User_id: {user_id}, JSON Generation Failed."


@app.get("/")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:app", host="0.0.0.0", port=9898, reload=True)
