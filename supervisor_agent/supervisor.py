from langgraph_supervisor import create_supervisor
from worker_agents import (llm, 
                           nomad_visa_agent, 
                           investment_visa_agent, 
                            startup_visa_agent, 
                            tourist_visa_agent, 
                            employment_visa_agent, 
                            expand_existing_business_visa_agent)


from prompt import supervisor_prompt

# from handoff_tools import transfer_to_investment_visa_agent, transfer_to_nomad_visa_agent

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



next_country_supervisor = create_supervisor(
    model=llm,
    agents=[nomad_visa_agent, 
            investment_visa_agent,
            startup_visa_agent, 
            tourist_visa_agent, 
            employment_visa_agent, 
            expand_existing_business_visa_agent
            ],
    prompt=supervisor_prompt,
    add_handoff_back_messages=True,
    output_mode="full_history",
).compile()


# with open("graph.png", "wb") as f:
#     f.write(next_country_supervisor.get_graph().draw_mermaid_png())