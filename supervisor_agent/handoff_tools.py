from langchain_core.tools import tool
from langgraph.types import Command
from langchain_core.tools import InjectedToolCallId
from langgraph.prebuilt import InjectedState

from typing import Annotated

def prepare_agent_input(agent_name: str, state: dict) -> dict:
    if agent_name == "nomad_visa_agent":
        # Extract and format only the fields needed by nomad_visa_agent
        return {
            "main_goal": state.get("main_goal", ""),
            "nationality": state.get("nationality", ""),
            "additional_passport": state.get("additional_passport", ""),
            "additional_residency": state.get("additional_residency", ""),
            "current_work_situation": state.get("current_work_situation", ""),
            "current_job_industry": state.get("current_job_industry", ""),
            "company_registered_at_home": state.get("company_registered_at_home", ""),
            "will_open_company_at_abroad": state.get("will_open_company_at_abroad", ""),
            "monthly_income": state.get("monthly_income", ""),
            "personal_savings": state.get("personal_savings", ""),
            "destination_country": state.get("destination_country", ""),
            "duration_of_stay": state.get("duration_of_stay", ""),
            "tax_benefits_option": state.get("tax_benefits_option", ""),
            "help_open_bank_account": state.get("help_open_bank_account", ""),
            "extend_stay_option": state.get("extend_stay_option", ""),
            "solo_or_family": state.get("solo_or_family", ""),
            "number_of_dependents": state.get("number_of_dependents", ""),
            "accomodation_help": state.get("accomodation_help", ""),
            "flight_booking_help": state.get("flight_booking_help", ""),
            "visa_denied_previously": state.get("visa_denied_previously", ""),
            "criminal_record": state.get("criminal_record", ""),
        }
    

    elif agent_name == "investment_visa_agent":
        # Extract and format only the fields needed by investment_visa_agent
        return {
            "main_goal": state.get("main_goal", ""),
            "nationality": state.get("nationality", ""),
            "additional_passport": state.get("additional_passport", ""),
            "additional_residency": state.get("additional_residency", ""),
            "primary_reason_for_investment": state.get("primary_reason_for_investment", ""),
            "long_term_goal": state.get("long_term_goal", ""),
            "interested_region_to_invest": state.get("interested_region_to_invest", ""),
            "investment_amount": state.get("investment_amount", ""),
            "liquid_cash_amount": state.get("liquid_cash_amount", ""),
            "financing_plan": state.get("financing_plan", ""),
            "require_financing_options": state.get("require_financing_options", ""),
            "type_of_investment_preferred": state.get("type_of_investment_preferred", ""),
            "passive_or_active_investment": state.get("passive_or_active_investment", ""),
            "current_business_status": state.get("current_business_status", ""),
            "years_of_operation": state.get("years_of_operation", ""),
            "annual_revenue": state.get("annual_revenue", ""),
            "monthly_income": state.get("monthly_income", ""),
            "solo_or_family": state.get("solo_or_family", ""),
            "number_of_dependents": state.get("number_of_dependents", ""),
            "primary_tax_objective": state.get("primary_tax_objective", ""),
            "urgency_for_residence": state.get("urgency_for_residence", ""),
            "relocate_to_investment_country": state.get("relocate_to_investment_country", ""),
            "visa_denied_previously": state.get("visa_denied_previously", ""),
            "criminal_record": state.get("criminal_record", ""),
        }
    else:
        # Default fallback: pass full state or empty dict
        return state





def create_handoff_tool(agent_name: str):
    @tool(f"transfer_to_{agent_name}")
    def handoff_tool(
        state: Annotated[dict, InjectedState],
        tool_call_id: Annotated[str, InjectedToolCallId],
    ) -> Command:
        """Prepare the state payload specific to the agent
        """
        agent_input = prepare_agent_input(agent_name, state)
        return Command(
            goto=agent_name,
            update=agent_input,
            graph=Command.PARENT,
        )
    return handoff_tool


transfer_to_nomad_visa_agent = create_handoff_tool(agent_name="nomad_visa_agent")
transfer_to_investment_visa_agent = create_handoff_tool(agent_name="investment_visa_agent")
