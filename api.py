from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.messages import AIMessage
import re

from rich import print, console

from supervisor_agent.supervisor import next_country_supervisor
from supervisor_agent.output_agent import output_agent


class NextCountryRequest(BaseModel):
    message:str


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

    supervisor_response = next_country_supervisor.invoke({"messages": data})
    for m in supervisor_response["messages"]:
        m.pretty_print()

    ai_response = [m for m in supervisor_response["messages"] if isinstance(m, AIMessage)]
    pretty_response = [m.content for m in ai_response]

    # print("Supervisor agent response: ", pretty_response)

    output_response = output_agent.invoke({"messages": pretty_response})

    output = output_response["messages"][-1].content

    # Extract JSON content
    json_content = re.sub(r'^```json\s*|\s*```$', '', output, flags=re.MULTILINE)
    print("Final JSON response: ", json_content.strip())

    return json_content.strip()



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app",
                host="localhost",
                port=9898, 
                reload=True)
