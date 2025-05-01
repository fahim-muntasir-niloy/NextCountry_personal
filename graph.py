from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_tool_calling_agent, AgentExecutor

import os
from dotenv import load_dotenv
load_dotenv()

from state import UserState, NC_AgentResponse
from prompt import prompt, parser
from tools import search_tavily, save_report

llm = ChatGoogleGenerativeAI(
    temperature=0.5,
    model="gemini-1.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY")
)

agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=[search_tavily, save_report]
)

agent_executor = AgentExecutor(agent=agent,
                               tools=[search_tavily, save_report],
                               max_iterations=5,
                               return_intermediate_steps=True,
                               handle_parsing_errors=True
                               )

raw_response = agent_executor.invoke(
    {
    "messages": """I am from Bangladesh and looking to do MSc in a Schengen country in Physics.
     I have BSc GPA of 2.7 and MSc GPA 3.8/4 and I am interested in Quantum Computing. 
     I have 2 years of research experience and published 10 papers.
     I have 2 years of work experience as a ML engineer.
     My IELTS score is 8.
     I am looking for universities that offer scholarships.
     Give me a list of 5 universities with their details."""
     }
)

# try:
#     structured_response = parser.parse(raw_response["output"])
# except Exception as e:
#     print(f"Error parsing response: {e}")
#     structured_response = None

# print(structured_response.model_dump_json(indent=4))
from save_report import save_report
save_report(raw_response)