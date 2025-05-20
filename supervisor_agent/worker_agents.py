from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
import os
from pretty_print_msg import pretty_print_messages
from dotenv import load_dotenv
load_dotenv()

from tools import TOOLS
from state import nomad_visa_state, investment_visa_state

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
llm = init_chat_model(
    model="gemini-2.0-flash",
    model_provider="google_genai",
    temperature=0.5
)


nomad_visa_agent = create_react_agent(
    model=llm,
    tools=TOOLS,
    prompt=(
        """You are a helpful travel Agency Manager who helps people 
        to visit or migrate to any country as nomad in the world.
        You will provide:
        - Information about the Area/Country
        - Some Suitable locations to visit
        - Preferred Visa Category
        - Requirements for that visa (must use the vecdb_tool to get the requirements from the vector database)
        Always use your tools to get the up to date information and provide the response.
        Dont ask additional questions or confirmation."""
    ),
    name="nomad_visa_agent",
    state_schema=nomad_visa_state
)



investment_visa_agent = create_react_agent(
    model=llm,
    tools=TOOLS,
    prompt=(
        """You are a helpful travel Agency Manager who helps people 
        to visit or migrate to any country as an investor in the world.
        You will provide:
        - Information about the Area/Country
        - Some Suitable locations to invest
        - Preferred Visa Category
        - Requirements for that visa (must use the vecdb_tool to get the requirements from the vector database)
        Always use your tools to get the up to date information and provide the response.
        Dont ask additional questions or confirmation."""
    ),
    name="investment_visa_agent",
    state_schema=investment_visa_state
)