import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from graph import graph

response = graph.invoke(
    {"messages":"Generate a response for the user based on the user details and query.",
     
        "main_goal": "Startup builder wanting to expand business in UK",
        "current_nationality": "Bangladesh",
        "additional_passport": False,
        "additional_residency": False,
        "current_work_situation": "Owner",
        "current_job_industry": "Fintech",
        "company_registered_at_home": True,
        "will_open_company_at_abroad": False,
        "monthly_income": "5000",
        "savings_in_personal_account": "150000",
        "interested_region": "Europe",
        "duration_of_stay": "3 years",
        "tax_benefits_option": True,
        "help_open_bank_account": True,
        "extend_stay_option": True,
        "solo_or_family": "Solo",
        "number_of_dependents": "4",
        "accommodation_in_new_country": True,
        "flight_status": True,
        "past_immigration_issue": False,
        "criminal_record": False
    }
)

# for m in response["messages"]:
#     m.pretty_print()


# save md file
from utils.save_report import save_report
save_report(response)

