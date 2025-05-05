from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.messages import AIMessage, ToolMessage, AnyMessage
from langgraph.graph import StateGraph, START

import os
from dotenv import load_dotenv
load_dotenv()

from state import NC_UserResponse, NC_AgentResponse
from prompt import prompt, parser
from tools import search_tavily, search_exa

llm = ChatGoogleGenerativeAI(
    temperature=0.5,
    model="gemini-1.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY")
)

agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=[search_tavily, search_exa]
)

agent_executor = AgentExecutor(agent=agent,
                               tools=[search_tavily, search_exa],
                               max_iterations=5,
                               return_intermediate_steps=True,
                               handle_parsing_errors=True
                               )

# raw_response = agent_executor.invoke(
#     {
#     "messages": """I am from Bangladesh and looking to do MSc in a Schengen country in Chemistry.
#      I have BSc GPA of 3.5 and MSc GPA 3.8/4 and I am interested in Nanotechnology. 
#      I have 2 years of research experience and published 3 papers.
#      My IELTS score is 8.
#      I am looking for universities that offer scholarships.
#      Give me a list of 5 universities with their details."""
#      }
# )

def call_agent(state:NC_UserResponse):
    main_goal = state.get("main_goal")
    current_nationality = state.get("current_nationality")
    additional_passport = state.get("additional_passport")
    additional_residency = state.get("additional_residency")
    current_work_situation = state.get("current_work_situation")
    current_job_industry = state.get("current_job_industry")
    company_registered_at_home = state.get("company_registered_at_home")
    will_open_company_at_abroad = state.get("will_open_company_at_abroad")
    monthly_income = state.get("monthly_income")
    savings_in_personal_account = state.get("savings_in_personal_account")
    interested_region = state.get("interested_region")
    duration_of_stay = state.get("duration_of_stay")
    tax_benefits_option = state.get("tax_benefits_option")
    help_open_bank_account = state.get("help_open_bank_account")
    extend_stay_option = state.get("extend_stay_option")
    solo_or_family = state.get("solo_or_family")
    number_of_dependents = state.get("number_of_dependents")
    accommodation_in_new_country = state.get("accommodation_in_new_country")
    flight_status = state.get("flight_status")
    past_immigration_issue = state.get("past_immigration_issue")
    criminal_record = state.get("criminal_record")
    
    messages = f"""
    My main goal is to: {main_goal}
    My current nationality is: {current_nationality}
    I have additional passport: {additional_passport}
    I have additional residency: {additional_residency}
    My current work situation is: {current_work_situation}
    My current job industry is: {current_job_industry}
    My company is registered at home: {company_registered_at_home}
    I will open company at abroad: {will_open_company_at_abroad}
    My monthly income is: {monthly_income}
    My savings in personal account is: {savings_in_personal_account}
    My interested region is: {interested_region}
    My duration of stay is: {duration_of_stay}
    I want tax benefits option: {tax_benefits_option}
    I need help to open bank account: {help_open_bank_account}
    I need extend stay option: {extend_stay_option}
    I am solo or family: {solo_or_family}
    My number of dependents is: {number_of_dependents}
    I need accommodation in new country: {accommodation_in_new_country}
    My flight status is: {flight_status}
    I have past immigration issue: {past_immigration_issue}
    I have criminal record: {criminal_record}
    """
    
    result = agent_executor.invoke({"messages": messages})

    messages = []
    for action, observation in result["intermediate_steps"]:
        messages.append(action.message_log[0])
        messages.append(ToolMessage(content=str(observation),
                                    tool_call_id=action.tool_call_id))
    messages.append(AIMessage(content=result["output"]))
    return {"messages": messages}
    
    
builder = StateGraph(NC_UserResponse)
builder.add_node(call_agent)
builder.add_edge(START, "call_agent")
graph = builder.compile()

response = graph.invoke(
    {"messages":"Generate a response for the user based on the user details and query.",
        "main_goal": "Relocate to a Schengen country",
        "current_nationality": "Bangladesh",
        "additional_passport": True,
        "additional_residency": False,
        "current_work_situation": "Employed",
        "current_job_industry": "IT",
        "company_registered_at_home": True,
        "will_open_company_at_abroad": False,
        "monthly_income": "5000",
        "savings_in_personal_account": "15000",
        "interested_region": "Europe",
        "duration_of_stay": "1 year",
        "tax_benefits_option": True,
        "help_open_bank_account": True,
        "extend_stay_option": True,
        "solo_or_family": "Solo",
        "number_of_dependents": "0",
        "accommodation_in_new_country": True,
        "flight_status": True,
        "past_immigration_issue": False,
        "criminal_record": False
    }
)

for m in response["messages"]:
    m.pretty_print()

# print(structured_response.model_dump_json(indent=4))
# from save_report import save_report
# save_report(response)