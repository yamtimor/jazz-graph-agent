from dataclasses import dataclass
from typing import Dict, Any
from langchain_core.tools import tool
import requests
from bs4 import BeautifulSoup
from config import CONFIG


@tool
def fetch_jazz_data(musician_name: str) -> str:
    """
    Fetch jazz musician collaboration data from jazzdisco.org or MusicBrainz API.
    
    Args:
        musician_name: Name of the jazz musician to search for
        
    Returns:
        Raw text containing musician collaboration information
    """
    # Try MusicBrainz API first
    try:
        # MusicBrainz API endpoint
        url = "https://musicbrainz.org/ws/2/artist/"
        params = {
            "query": f'artist:"{musician_name}" AND tag:jazz',
            "fmt": "json",
            "limit": 1
        }
        headers = {"User-Agent": "JazzGraphAgent/1.0"}
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("artists"):
            artist = data["artists"][0]
            artist_id = artist.get("id")
            artist_name = artist.get("name")
            
            # Get recording relationships
            rel_url = f"https://musicbrainz.org/ws/2/artist/{artist_id}"
            rel_params = {"inc": "recordings+artist-rels", "fmt": "json"}
            rel_response = requests.get(rel_url, params=rel_params, headers=headers, timeout=10)
            rel_response.raise_for_status()
            
            rel_data = rel_response.json()
            
            # Format the response
            result = f"Artist: {artist_name}\n\n"
            result += "Collaborations and Recordings:\n"
            
            if "relations" in rel_data:
                for relation in rel_data["relations"][:20]:  # Limit to 20 relations
                    if relation.get("type") == "member of band":
                        target = relation.get("artist", {})
                        result += f"- Member of: {target.get('name', 'Unknown')}\n"
                    elif relation.get("type") in ["collaboration", "performance"]:
                        target = relation.get("artist", {})
                        result += f"- Collaborated with: {target.get('name', 'Unknown')}\n"
            
            return result if len(result) > 100 else f"Found artist {artist_name} but no detailed collaboration data available from MusicBrainz."
        
        return f"No data found for musician: {musician_name}"
        
    except Exception as e:
        # Fallback: return structured mock data for development
        return f"""Artist: {musician_name}

Collaborations and Recordings:
Note: Using mock data as API fetch failed ({str(e)[:50]})

Sample Bebop Era Collaborations:
- Collaborated with: Dizzy Gillespie (trumpet, 1945-1955)
- Collaborated with: Miles Davis (trumpet, 1945-1948)
- Collaborated with: Max Roach (drums, 1945-1955)
- Collaborated with: Bud Powell (piano, 1947-1953)
- Member of: Charlie Parker Quintet
- Session with: J.J. Johnson (trombone, 1947)
- Session with: Sonny Stitt (alto sax, 1950)
- Recorded with: Tommy Potter (bass, 1947-1950)
- Recorded with: Roy Haynes (drums, 1949-1952)

This is sample data to demonstrate the pipeline. Implement actual API/scraping for production use."""


@tool
def parse_jazz_data(raw_text: str, seed_musician: str, era_start: int, era_end: int) -> Dict[str, Any]:
    """
    Parse raw jazz data text and extract musician relationships as a graph structure.
    This is a placeholder - the actual parsing will be done by the LLM agent.
    
    Args:
        raw_text: Raw text containing musician collaboration information
        seed_musician: The primary musician being analyzed
        era_start: Start year of the era filter
        era_end: End year of the era filter
        
    Returns:
        Dictionary with 'nodes' and 'edges' lists representing the musician network
    """
    # This is a placeholder that will be replaced by LLM-driven extraction
    # The agent will use this tool with structured output
    return {
        "nodes": [
            {"id": seed_musician, "instrument": "primary"}
        ],
        "edges": []
    }


@dataclass
class Context:
    """Custom runtime context schema."""
    user_id: str


