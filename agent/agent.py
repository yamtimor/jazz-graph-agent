from langchain.agents import create_agent
from model import model
from prompts import SYSTEM_PROMPT, ResponseFormat
from tools import Tools, Context
from config import CONFIG


agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=Tools,
    context_schema=Context,
    response_format=ResponseFormat,
)

# `thread_id` is a unique identifier for a given conversation.
config = {"configurable": {"thread_id": "1"}}

response = agent.invoke(
    {"messages": [{"role": "user", "content": "a placeholder message"}]},
    config=config,
    context=Context(user_id="1")
)

print(response['structured_response'])

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

    # ---------------------------
    # 1. Fetch raw data (tool)
    # ---------------------------
    raw_text = fetch_jazz_data(musician)

    # ---------------------------
    # 2. Parse raw text into JSON
    # ---------------------------
    graph_json = parse_jazz_data(
        raw_text=raw_text,
        seed_musician=musician,
        era_start=start_year,
        era_end=end_year,
    )

    # graph_json must be of shape:
    # {
    #   "nodes": [{"name": "..."} , ...],
    #   "edges": [{"source": "...", "target": "..."} , ...]
    # }

    return graph_json