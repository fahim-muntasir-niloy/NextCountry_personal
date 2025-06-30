from langgraph_supervisor import create_supervisor
from supervisor_agent.tools import TOOLS


from supervisor_agent.worker_agents import (llm,
                                            nomad_visa_agent, 
                                            investment_visa_agent, 
                                            startup_visa_agent, 
                                            tourist_visa_agent, 
                                            employment_visa_agent, 
                                            expand_existing_business_visa_agent)


from supervisor_agent.prompt import supervisor_prompt

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



next_country_supervisor = create_supervisor(
    model=llm,
    agents=[
            nomad_visa_agent, 
            investment_visa_agent,
            startup_visa_agent, 
            tourist_visa_agent, 
            employment_visa_agent, 
            expand_existing_business_visa_agent
            ],
    prompt=supervisor_prompt,
    tools = TOOLS,
    add_handoff_back_messages=False,
    output_mode="full_history",
    parallel_tool_calls = False,
    supervisor_name="Next Country Supervisor",
).compile()


# with open("graph.png", "wb") as f:
#     f.write(next_country_supervisor.get_graph().draw_mermaid_png())