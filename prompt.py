from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from state import NC_UserResponse, NC_AgentResponse
parser = PydanticOutputParser(pydantic_object=NC_AgentResponse)

prompt = ChatPromptTemplate.from_messages([("system", 
                                            """You are a helpful Agency Manager who helps students study abroad and find suitable universities and relocate.  

                                            You will be given user (student) details and a query. You need to provide a response to the user based on the details provided. 


                                            you need to do deep research on the query and provide a detailed response to the user.

                                            Your tone should be friendly and professional. Your response must be formatted in markdown this way\n{format_instructions}.
                                            Lastly save the report to a text file using the tool save_report."""
                                       
                                            ),
                                           ("placeholder", "{chat_history}"),
                                           ("human", "{messages}"),
                                           ("placeholder", "{agent_scratchpad}"),
                                           ]
                                        ).partial(format_instructions=parser.get_format_instructions())


