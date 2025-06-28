import os
from dotenv import load_dotenv
load_dotenv()

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model

client = MultiServerMCPClient(
    {
        "NC_Chatbot_Server": {
            "command": "python",
            # Make sure to update to the full absolute path to your math_server.py file
            "args": ["/home/fahim-muntasir/Office/NextCountry_personal/chatbot/server.py"],
            "transport": "stdio",
        }
    }
)

llm = init_chat_model("google_genai:gemini-2.5-flash", temperature=0.7)

async def init_chat(msg):
    tools = await client.get_tools()
    agent = create_react_agent(llm, tools)
    
    res = await agent.ainvoke({
        "messages":msg
    })

    return res


import asyncio

response = asyncio.run(
    init_chat("/kb I am afraid to take english test, where can I go?")
)

for m in response["messages"]:
    m.pretty_print()

