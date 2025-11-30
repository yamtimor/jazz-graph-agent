from typing import Dict, Any, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, SystemMessage
import instructor
from agent.model import model, get_raw_client
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
    try:
        print(f"Fetching data for {state['musician_name']}...")
        raw_data = fetch_jazz_data.invoke({"musician_name": state["musician_name"]})
        
        if not raw_data or len(raw_data.strip()) == 0:
            raise ValueError(f"No data returned for musician: {state['musician_name']}")
            
        state["raw_data"] = raw_data
        return state
    except Exception as e:
        print(f"Error fetching data: {e}")
        raise


def parse_data_node(state: AgentState) -> AgentState:
    """Node that uses LLM to parse raw data into structured graph."""
    try:
        print("Parsing data with LLM...")
        
        if not state.get("raw_data"):
            raise ValueError("No raw data available to parse")
        
        # Create prompt for LLM
        user_message = f"""Please analyze the following data about {state['musician_name']} and extract a collaboration network.

Focus on collaborations between {state['era_start']} and {state['era_end']}.

Raw Data:
{state['raw_data']}

Extract all musicians and their collaboration relationships. Create a graph structure with:
- nodes: list of musicians with their instruments
- edges: list of collaboration relationships between musicians
"""
        
        # Use Instructor for structured output across providers
        provider = CONFIG.llm_provider
        
        if provider == "openai":
            # Use OpenAI with Instructor
            client = get_raw_client(provider)
            instructor_client = instructor.from_openai(client)
            
            result = instructor_client.chat.completions.create(
                model=CONFIG.llm_model,
                response_model=ResponseFormat,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=CONFIG.max_tokens,
                temperature=0,
            )
        
        elif provider == "huggingface":
            # Use HuggingFace with Instructor
            from instructor import Mode
            client = get_raw_client(provider)
            instructor_client = instructor.from_huggingface(client, mode=Mode.JSON)
            
            # Combine system and user messages for HF
            combined_message = f"{SYSTEM_PROMPT}\n\n{user_message}"
            
            result = instructor_client.chat.completions.create(
                model=CONFIG.llm_model,
                response_model=ResponseFormat,
                messages=[
                    {"role": "user", "content": combined_message}
                ],
                max_tokens=CONFIG.max_tokens,
                temperature=0,
            )
        
        else:
            raise ValueError(f"Unsupported provider: {provider}")
        
        if not result or not hasattr(result, 'nodes'):
            raise ValueError("LLM did not return valid structured output")
        
        # Convert Pydantic models to dict
        graph_data = {
            "nodes": [{"id": node.id, "instrument": node.instrument, "role": node.role} 
                      for node in result.nodes],
            "edges": [{"source": edge.source, "target": edge.target, 
                       "collaboration_type": edge.collaboration_type, "weight": edge.weight}
                      for edge in result.edges]
        }
        
        print(f"Extracted {len(graph_data['nodes'])} nodes and {len(graph_data['edges'])} edges")
        
        state["graph_data"] = graph_data
        return state
        
    except Exception as e:
        print(f"Error parsing data: {e}")
        raise


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
    
    Raises:
        ValueError: If musician name is invalid or data cannot be processed
        Exception: For any other errors during agent execution
    """
    try:
        musician = seed_musician or CONFIG.seed_musician
        start_year = era_start_year or CONFIG.era_start_year
        end_year = era_end_year or CONFIG.era_end_year
        
        if not musician or not isinstance(musician, str):
            raise ValueError(f"Invalid musician name: {musician}")
        
        if start_year >= end_year:
            raise ValueError(f"Invalid era: start_year ({start_year}) must be less than end_year ({end_year})")
        
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
        
        if not result.get("graph_data"):
            raise ValueError("Agent did not produce graph data")
        
        return result["graph_data"]
        
    except Exception as e:
        print(f"\nError running jazz agent: {e}")
        raise