from dataclasses import dataclass
from langchain.tools import tool, ToolRuntime

@tool
def fetch_jazz_data(query: str) -> str:
    """Fetch jazz data from the web"""
    return "Jazz data"
@dataclass
class Context:
    """Custom runtime context schema."""
    user_id: str

@tool
def parse_jazz_data(raw_text: str) -> str:
    """Parse jazz data from raw text"""
    return "Jazz data"


