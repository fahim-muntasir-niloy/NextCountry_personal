import os
from dotenv import load_dotenv

load_dotenv()

from langgraph.graph import StateGraph, START, MessagesState
from langchain_core.messages import AnyMessage

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model

client = MultiServerMCPClient(
    {
        "NC_Chatbot_Server": {
            "command": "python",
            "args": ["D:\\NextCountry_personal\\chatbot\\server.py"],
            "transport": "stdio",
        }
    }
)

llm = init_chat_model("google_genai:gemini-2.5-flash", temperature=0.7)


# Define custom state schema with messages and user_id
class CustomState(MessagesState):
    user_id: str
    remaining_steps: list


# Optional: define a prompt function that can access the custom state
def prompt(state: CustomState):
    user_id = state["user_id"]
    system_msg = f"""You are a funny and helpful assistant. 
                    keep your answer short and to the point.
                    Always use the knowledgebase tool to get the information, whether user tells you to or not.
                    Try to answer in 6-10 sentances maximum.
                    Use emojis in response.
                    You must breakdown the user query and pass it multiple times to knowledgebase tool for better response.
                    eg: compare between morocco and Mauritius investor visa documents
                    flow: you will first find morocco visa documents, then mauritius visa documents. Then prepare the answer.
                    The current User ID is {user_id}."""

    return [{"role": "system", "content": system_msg}] + state["messages"]


# Create the agent with the custom state schema and prompt


async def init_chat(msg, user_id):
    tools = await client.get_tools()

    agent = create_react_agent(
        model=llm,
        tools=tools,
        state_schema=CustomState,
        prompt=prompt,
    )

    res = await agent.ainvoke({"messages": msg, "user_id": user_id})

    return res["messages"][-1].content


# import asyncio

# response = asyncio.run(
#     init_chat(
#         "Compare between portugal and lithuania startup visas? Will UAE be safer for easy access?",
#         "2adaf9b0-3183-411d-a916-f788626709cb",
#     )
# )

# for m in response["messages"]:
#     m.pretty_print()
