from state import NC_UserResponse
from langchain_core.messages import AIMessage, ToolMessage
from agent_utils.executor import agent_executor


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


    #  add intermediate steps to the messages
    messages = []
    for action, observation in result["intermediate_steps"]:
        messages.append(action.message_log[0])
        messages.append(ToolMessage(content=str(observation),
                                    tool_call_id=action.tool_call_id))
    messages.append(AIMessage(content=result["output"]))
    return {"messages": messages}