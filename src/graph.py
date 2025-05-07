from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

import os
from dotenv import load_dotenv
load_dotenv()

from state import NC_UserResponse, NC_AgentResponse
from agent_utils.agent import call_agent
from tools import search_tavily, search_exa, vecdb_tool


# === Tools ===
tools = [search_tavily, search_exa, vecdb_tool]

    
# === Graph ===
builder = StateGraph(NC_UserResponse)

builder.add_node("call_agent", call_agent)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "call_agent")
builder.add_conditional_edges(
    "call_agent",
    tools_condition,
)
builder.add_edge("tools", "call_agent")

graph = builder.compile()

print(graph.get_graph().draw_ascii())