from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.messages import AIMessage
import re
import json

from rich import print, console

from supervisor_agent.supervisor import next_country_supervisor
from supervisor_agent.output_agent import output_agent
from utils.save_report import save_report


class NextCountryRequest(BaseModel):
    message:dict


app = FastAPI(
    title="Next Country API",
    description="API for the Next Country project",
    version="0.1.0",
    contact={
        "name": "Fahim Muntasir",
        "url": "https://nextcountry.com",
    }
)

@app.post("/next_country")
def json_output_flow(request: NextCountryRequest):
    data = request.message
    print("Received message: ", data)
    
    # Handling input json -> make it string
    pretty_json_str = json.dumps(data, indent=4)
    escaped_json_str = pretty_json_str.replace('\n', '\\n').replace('"', '\\"')

    supervisor_response = next_country_supervisor.invoke({"messages": escaped_json_str})
    
    for m in supervisor_response["messages"]:
        m.pretty_print()
        
    save_report(supervisor_response)

    ai_response = [m for m in supervisor_response["messages"] if isinstance(m, AIMessage)]
    pretty_response = [m.content for m in ai_response]

    # print("Supervisor agent response: ", pretty_response)

    output_response = output_agent.invoke({"messages": pretty_response})

    output = output_response["messages"][-1].content
    
    # print(output)

    # Handling output string -> convert to json
    json_match = re.search(r"```json\n(.*?)```", output, re.DOTALL)
    if json_match:
        json_str = json_match.group(1)
        clean_json = json.loads(json_str)
        print(clean_json)
        return clean_json
    
    else:
        print("No JSON block found.")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app",
                host="localhost",
                port=9898, 
                reload=True)
