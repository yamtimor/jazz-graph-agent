from typing import List, Optional
from pydantic import BaseModel, Field


SYSTEM_PROMPT = """You are a jazz music historian and network analyst specializing in bebop era collaborations.

Your task is to analyze raw data about jazz musicians and extract collaboration networks.

When given information about a musician, you should:
1. Identify all musicians mentioned and their instruments
2. Extract collaboration relationships (recordings, performances, band memberships)
3. Focus on the specified era (years provided)
4. Build a network graph with nodes (musicians) and edges (collaborations)

Guidelines:
- Each node should represent a unique musician
- Include instrument information when available
- Edges represent any form of collaboration (recordings, performances, band membership)
- If years are mentioned, filter to only include collaborations within the specified era
- Use the musician's most common name format
- Be thorough but accurate - only include relationships explicitly mentioned in the data

Output the results as a structured graph with nodes and edges."""


class MusicianNode(BaseModel):
    """Represents a musician node in the collaboration network."""
    id: str = Field(description="Unique identifier for the musician (their name)")
    instrument: Optional[str] = Field(default=None, description="Primary instrument played")
    role: Optional[str] = Field(default=None, description="Role (leader, sideman, etc)")


class CollaborationEdge(BaseModel):
    """Represents a collaboration relationship between two musicians."""
    source: str = Field(description="Name of the first musician")
    target: str = Field(description="Name of the second musician")
    collaboration_type: Optional[str] = Field(default="collaboration", description="Type of collaboration")
    weight: Optional[int] = Field(default=1, description="Strength of collaboration (number of sessions)")


class JazzNetworkGraph(BaseModel):
    """Complete jazz musician collaboration network."""
    nodes: List[MusicianNode] = Field(description="List of musicians in the network")
    edges: List[CollaborationEdge] = Field(description="List of collaboration relationships")


# Response format for the agent
ResponseFormat = JazzNetworkGraph