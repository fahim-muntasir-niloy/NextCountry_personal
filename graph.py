from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_tool_calling_agent, AgentExecutor

import os
from dotenv import load_dotenv
load_dotenv()

from state import UserState, NC_AgentResponse
from prompt import prompt
# from save_report import save_report

llm = ChatGoogleGenerativeAI(
    temperature=0.5,
    model="gemini-1.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY")
)

agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=[]
)

agent_executor = AgentExecutor(agent=agent,
                               tools=[],
                               return_intermediate_steps=True,
                               handle_parsing_errors=True
                               )

response = agent_executor.invoke(
    {
    "messages": """I am looking to study in a Schengen country for my master's degree in computer science.
     I have a GPA of 3.5 and I am interested in AI and machine learning. 
     I have some research experience and I am looking for universities that offer scholarships."""
     }
)

print(response["output"])