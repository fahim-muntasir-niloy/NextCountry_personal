import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from supervisor_agent.supervisor import next_country_supervisor

response = next_country_supervisor.invoke(
    {
        "messages": 
    """
    "Q1: What is your main goal?": "Expand/Relocate Existing Business",
    "Q2: What is your Budget/Investment Level?": "50k - 200k USD",
    "Q3: What is your Language Requirements?": "I don’t speak English",
    "Q4: What is your Family Situation?": "Married ( No Children )",
    "Q5: What is your Timeframe/Urgency?": "Flexible ( 6 - 12 months)",
    "Q6: Geographic Preference?": "Open to Suggestions",
    "Q7: Any Preferred Countries?": "American Samoa",
    "Q8: Your Current Business Registration?": "Not officially registered yet",
    "Q9: What is your Industry/Sector?": "Services / Consulting / Agency",
    "Q10: Company Ownership Structure?": "Ownership split among multiple partners",
    "Q11: Number of Employees?": "250+",
    "Q12: Annual Revenue (Approx.)?": "$100,000–$500,000",
    "Q13: Budget for Expansion?": "$50k–$200k",
    "Q14: Expansion Timeline?": "3–6 months",
    "Q15: Preferred Region?": "Open to any region",
    "Q16: Family Relocation?": "Me + spouse",
    "Q17: Long-Term Goals?": "Still exploring options",
    "Q18: Previous International Experience?": "Never expanded abroad",
    "Q19: Relocation Scope?": "Founder + key management team",
    "Q20: Are You Able to live for a Period of 180 days in a year?": "LET’S TALK"
    """
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