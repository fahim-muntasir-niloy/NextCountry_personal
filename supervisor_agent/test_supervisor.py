import os, sys
import asyncio
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from supervisor_agent.supervisor import next_country_supervisor

response = next_country_supervisor.invoke(
    {
        "messages": 
    """
    {
    "Q1: What is your main goal?": "Employment",
    "Q2: What is your nationality?": "Albania",
    "Q3: Do you hold any additional passports?": "no",
    "Q4: Do you currently have residency or citizenship in another country?": "no",
    "Q5: What is your highest level of education?": "Vocational/Technical Certification",
    "Q6: What is your current job title?": "Machine Learning Engineer",
    "Q7: How many years of work experience do you have in this field?": "10+ Years",
    "Q8: Do you have a job offer from an employer abroad?": "No, but I plan to apply once I get the visa",
    "Q9: Does your employer sponsor work visas?": "No, I need to apply independently",
    "Q10: Are you applying alone or with family?": "With Spouse & Children",
    "Q11: How many dependents will be included in your application?": "More than 5",
    "Q12: Which regions are you interested in working in?": "No Preference – I’m open to recommendations",
    "Q13: What type of work visa are you looking for?": "Work & Residence Visa (Long-term immigration option)",
    "Q14: What is your current monthly salary?": "$10,000+",
    "Q15: What is your expected salary in your new country?": "$10,000+",
    "Q16: Do you have enough savings to support yourself during the visa process?": "No, I need financial assistance",
    "Q17: Are you willing to pay for government visa fees and relocation expenses?": "No, I need an employer to cover all costs",
    "Q18: What is your English proficiency level?": "Native Speaker",
    "Q19: Do you have an English language test certification?": "No, and I do not plan to take the test",
    "Q20: Have you ever been denied a visa or had immigration issues?": "Yes, and it was not resolved",
    "Q21: Do you or any of your dependents have a criminal record?": "no",
    "Q22: If a work visa is not available, would you consider alternative immigration options?": "No, I am only interested in employment visas",
    "Q23: How soon do you need to move for work?": "No rush, just exploring "
}
    """
    })

# from langchain_core.messages import AIMessage, HumanMessage

# msgs = [m for m in res["messages"] if isinstance(m, AIMessage)]

# for msg in msgs:
#     print(msg.content + "\n")  # or msg.pretty_print()

# for m in response["messages"]:
#     m.pretty_print()



from utils.save_report import save_report
save_report(response)