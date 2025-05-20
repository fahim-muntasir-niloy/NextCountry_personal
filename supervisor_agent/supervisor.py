from langgraph_supervisor import create_supervisor
from worker_agents import llm, nomad_visa_agent, investment_visa_agent
from pretty_print_msg import pretty_print_messages
from state import supervisor_state

from handoff_tools import transfer_to_investment_visa_agent, transfer_to_nomad_visa_agent

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



next_country_supervisor = create_supervisor(
    model=llm,
    agents=[nomad_visa_agent, 
            investment_visa_agent],
    prompt=(
        """
        You are a supervisor managing two agents:
        - a nomad visa agent. Assign nomad visa-related tasks to this agent.
        - an investment visa agent. Assign investment visa-related tasks to this agent.

        Always read the main_goal first. Based on that, delegate the task to the matching agent.

        Do not perform any work yourself except for basic conversation and task scheduling.

        When you receive the worker agent's response, do not simply confirm receipt or give generic messages.

        Instead, provide a detailed, thoughtful extension of the worker agent's output, elaborating and
        synthesizing the information as appropriate.

        Relay the full, enriched response back without adding any unrelated commentary or confirmation.

        Your output should be everything from the worker agent's response to the end, with seamless 
        continuation and enhancement of the worker agent's work.

        Your tone will be enthusiastic and friendly, like you have to close the deal.

        """
    ),
    tools=[transfer_to_nomad_visa_agent, transfer_to_investment_visa_agent],
    state_schema=supervisor_state,
    add_handoff_back_messages=True,
    output_mode="full_history",
).compile()


# with open("graph.png", "wb") as f:
#     f.write(next_country_supervisor.get_graph().draw_mermaid_png())


response = next_country_supervisor.invoke(
    {
        "messages": [
            {"role": "user", 
             "content": (
                "Main goal: Investment Programs\n"
                "Nationality: Algeria\n"
                "Additional passport: No\n"
                "Additional residency: No\n"
                "Primary reason for investment: Secure a Safe Future for My Family\n"
                "Long term goal: Build a real estate portfolio in a new country\n"
                "Interested region to invest: United Arab Emirates\n"
                "Investment amount: $1,000,000\n"
                "Liquid cash amount: $250,000 - $1 million\n"
                "Financing plan: Bank loan / Financing\n"
                "Require financing options: No\n"
                "Type of investment preferred: Real Estate Investment (Purchase property for residence or rental income)\n"
                "Passive or active investment: Active – I want to run my business in the new country\n"
                "Current business status: Both\n"
                "Years of operation: 3-5 years\n"
                "Annual revenue: $1 million - $5 million\n"
                "Monthly income: $15,000 - $50,000\n"
                "Solo or family: With Spouse & Children\n"
                "Number of dependents: 3-5\n"
                "Primary tax objective: Optimize Capital Gains & Wealth Tax\n"
                "Urgency for residence: 1-2 years\n"
                "Relocate to investment country: No, I prefer remote investment\n"
                "Visa denied previously: No\n"
                "Criminal record: Yes\n\n"
                "Please generate a response based on these details."
            )}
        ]
    }
)


# from langchain_core.messages import AIMessage, HumanMessage

# msgs = [m for m in response["messages"] if isinstance(m, AIMessage)]

# for msg in msgs:
#     print(msg.content)  # or msg.pretty_print()

for m in response["messages"]:
    m.pretty_print()


from utils.save_report import save_report
save_report(response)