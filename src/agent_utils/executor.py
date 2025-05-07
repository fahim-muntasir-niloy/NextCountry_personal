from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.chat_models import init_chat_model
from agent_utils.prompt import prompt

from tools import search_tavily, search_exa, vecdb_tool
import os

from dotenv import load_dotenv
load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

llm = init_chat_model(
    model="gemini-2.0-flash",
    model_provider="google_genai",
    temperature=0.5
)

# tools
tools = [search_tavily, search_exa, vecdb_tool]


agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(agent=agent,
                               tools=tools,
                               max_iterations=5,
                               return_intermediate_steps=True,
                               handle_parsing_errors=True
                               )
