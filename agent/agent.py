from typing import Dict, Any, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, SystemMessage
from agent.model import model
from agent.prompts import SYSTEM_PROMPT, ResponseFormat
from agent.tools import fetch_jazz_data
from config import CONFIG


class AgentState(TypedDict):
    """State for the jazz graph agent."""
    musician_name: str
    era_start: int
    era_end: int
    raw_data: str
    graph_data: Dict[str, Any]
    messages: list


def fetch_data_node(state: AgentState) -> AgentState:
    """Node that fetches raw jazz data."""
    print(f"Fetching data for {state['musician_name']}...")
    raw_data = fetch_jazz_data.invoke({"musician_name": state["musician_name"]})
    state["raw_data"] = raw_data
    return state


def parse_data_node(state: AgentState) -> AgentState:
    """Node that uses LLM to parse raw data into structured graph."""
    print("Parsing data with LLM...")
    
    # Create prompt for LLM
    user_message = f"""Please analyze the following data about {state['musician_name']} and extract a collaboration network.

Focus on collaborations between {state['era_start']} and {state['era_end']}.

Raw Data:
{state['raw_data']}

Extract all musicians and their collaboration relationships. Create a graph structure with:
- nodes: list of musicians with their instruments
- edges: list of collaboration relationships between musicians
"""
    
    # Use structured output with the LLM
    structured_llm = model.with_structured_output(ResponseFormat)
    
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_message)
    ]
    
    result = structured_llm.invoke(messages)
    
    # Convert Pydantic models to dict
    graph_data = {
        "nodes": [{"id": node.id, "instrument": node.instrument, "role": node.role} 
                  for node in result.nodes],
        "edges": [{"source": edge.source, "target": edge.target, 
                   "collaboration_type": edge.collaboration_type, "weight": edge.weight}
                  for edge in result.edges]
    }
    
    state["graph_data"] = graph_data
    return state


def build_agent_graph() -> StateGraph:
    """Build the LangGraph agent workflow."""
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("fetch_data", fetch_data_node)
    workflow.add_node("parse_data", parse_data_node)
    
    # Define the flow
    workflow.set_entry_point("fetch_data")
    workflow.add_edge("fetch_data", "parse_data")
    workflow.add_edge("parse_data", END)
    
    return workflow.compile()


# Create the agent
jazz_agent = build_agent_graph()


def run_jazz_agent(
    seed_musician: str | None = None,
    era_start_year: int | None = None,
    era_end_year: int | None = None,
) -> Dict[str, Any]:
    """
    High-level orchestrator for the jazz agent.
    Returns structured graph data: {"nodes": [...], "edges": [...]}
    """
    musician = seed_musician or CONFIG.seed_musician
    start_year = era_start_year or CONFIG.era_start_year
    end_year = era_end_year or CONFIG.era_end_year
    
    print(f"\n=== Jazz Graph Agent ===")
    print(f"Analyzing: {musician}")
    print(f"Era: {start_year}-{end_year}\n")
    
    # Initialize state
    initial_state = {
        "musician_name": musician,
        "era_start": start_year,
        "era_end": end_year,
        "raw_data": "",
        "graph_data": {},
        "messages": []
    }
    
    # Run the agent
    result = jazz_agent.invoke(initial_state)
    
    return result["graph_data"]