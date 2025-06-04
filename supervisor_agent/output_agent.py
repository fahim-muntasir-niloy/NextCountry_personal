from supervisor_agent.prompt import final_json_prompt
from supervisor_agent.tools import TOOLS

from supervisor_agent.worker_agents import llm
from langgraph.prebuilt import create_react_agent

output_agent = create_react_agent(
    model=llm,
    tools=TOOLS,
    prompt=final_json_prompt
)