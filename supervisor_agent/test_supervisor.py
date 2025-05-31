import os, sys
import asyncio
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from supervisor_agent.supervisor import next_country_supervisor

response = next_country_supervisor.invoke(
    {
        "messages": 
    """
{
    "Q1: What is your main goal?": "Digital Nomad",
    "Q2: What is your nationality?": "Albania",
    "Q3: Do you hold any additional passports?": "no",
    "Q4: Do you currently have residency or citizenship in another country?": "no",
    "Q5: What best describes your work situation?": "Other",
    "Q6: What industry do you work in?": "software development",
    "Q7: Do you work for a company registered in your home country?": "no",
    "Q8: Are you looking to open a company in your new country?": "No, I will continue working remotely",
    "Q9: What is your monthly income from remote work?": "Less than $1,500",
    "Q10: How much savings do you have in your personal account?": " $50,000+",
    "Q11: Which regions are you interested in moving to?": "Europe (Portugal, Spain, Estonia, etc.)",
    "Q12: How long do you plan to stay in your new country?": "Not sure",
    "Q13: Are you looking for tax benefits or financial optimization?": "No, tax benefits are not a priority",
    "Q14: Do you need help setting up a bank account in your new country?": "no",
    "Q15: Do you want the option to extend your stay or apply for residency?": "No, I plan to return home after my visa expires",
    "Q16: Are you applying alone or with family?": "With Spouse",
    "Q17: How many dependents will be included in your application?": "1-2",
    "Q18: Do you already have accommodation arranged in your new country?": "No, I need help finding a place",
    "Q19: Do you already have a flight booked?": "no",
    "Q20: Have you ever been denied a visa or had immigration issues?": "Yes, and it was not resolved",
    "Q21: Do you or any of your dependents have a criminal record?": "no"
}
    """
    })

# from langchain_core.messages import AIMessage, HumanMessage

# msgs = [m for m in res["messages"] if isinstance(m, AIMessage)]

# for msg in msgs:
#     print(msg.content + "\n")  # or msg.pretty_print()

for m in response["messages"]:
    m.pretty_print()

# from rich.console import Console
# from rich.markdown import Markdown

# console = Console()
# markdown = Markdown(response)
# console.print(markdown)

from utils.save_report import save_report
save_report(response)