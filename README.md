# jazz-graph-agent

An end-to-end LangGraph agent that fetches jazz musician data, extracts collaboration relationships using structured LLM output, and generates an interactive social network visualization with SNA metrics.

**Focus**: Bebop era (1940-1960), but the architecture supports any jazz domain.

---

## What This Project Does

`jazz-graph-agent` demonstrates a complete AI agent pipeline:

1. **Fetches** jazz musician data from MusicBrainz API (with mock fallback)
2. **Extracts** collaboration networks using LLM with structured output (Pydantic schemas)
3. **Builds** a NetworkX graph from the extracted relationships
4. **Computes** Social Network Analysis metrics (degree centrality, betweenness, clustering)
5. **Visualizes** the network as an interactive HTML graph (PyVis)

---

## Architecture

### Phase 1: LangGraph Agent (LLM-Driven)

A **LangGraph state machine** orchestrates two sequential nodes:

#### Node 1: `fetch_data_node`
- Calls `fetch_jazz_data(musician_name)` tool
- Attempts to fetch from MusicBrainz API
- Falls back to mock data for development/demo purposes
- Returns raw text with collaboration information

#### Node 2: `parse_data_node`
- Uses **LLM with structured output** (Pydantic models)
- Parses raw text into a validated `JazzNetworkGraph` schema:
  ```python
  {
    "nodes": [{"id": "musician_name", "instrument": "...", "role": "..."}],
    "edges": [{"source": "...", "target": "...", "collaboration_type": "...", "weight": 1}]
  }
  ```
- Filters collaborations by era (start/end years)
- Returns validated, structured graph data

**Key Technology**: LangGraph provides clear state management and sequential workflow control, making the agent logic explicit and debuggable.

---

### Phase 2: Pipeline (Deterministic Python)

Once structured data is extracted, pure Python processes it:

**`pipeline/graph_builder.py`**
- Converts JSON to NetworkX graph
- Validates nodes and edges
- Adds musician attributes (instrument, role)

**`pipeline/metrics.py`**
- Computes **degree centrality** (connection count)
- Computes **betweenness centrality** (bridging power)
- Computes **clustering coefficient** (local connectivity)

**`pipeline/visualize.py`**
- Generates interactive PyVis HTML
- Node size = degree centrality
- Hover tooltips show metrics
- Dark theme for readability

---

## Project Structure

```
jazz-graph-agent/
├── main.py                    # Entry point, orchestrates full pipeline
├── config.py                  # Configuration (musician, era, paths, LLM settings)
├── .env                       # Environment variables (OPENAI_API_KEY)
│
├── agent/
│   ├── agent.py              # LangGraph state machine and workflow
│   ├── tools.py              # fetch_jazz_data tool (MusicBrainz API + fallback)
│   ├── prompts.py            # System prompt and Pydantic schemas
│   └── model.py              # ChatOpenAI model configuration
│
├── pipeline/
│   ├── graph_builder.py      # JSON → NetworkX graph
│   ├── metrics.py            # SNA metric computation
│   └── visualize.py          # PyVis HTML generation
│
└── data/output/
    └── jazz_graph.html       # Final interactive visualization
```

---

## Setup & Installation

### Prerequisites
- Python 3.10+
- OpenAI API key

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd jazz-graph-agent
```

### 2. Create virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
# Optional: Override default model
# OPENAI_MODEL=gpt-4o-mini
```

### 5. Run the pipeline
```bash
python main.py
```

**Output**: 
- Console logs showing progress
- `data/output/jazz_graph.html` — open in browser to explore the network

---

## Configuration

Edit `config.py` to customize:

```python
@dataclass(frozen=True)
class JazzGraphConfig:
    # Choose your musician and era
    seed_musician: str = "Charlie Parker"
    era_start_year: int = 1940
    era_end_year: int = 1960
    
    # LLM settings
    llm_model: str = "gpt-4o-mini"
    max_tokens: int = 3000
```

---

## How It Works (Step-by-Step)

1. **Agent Initialization**
   - LangGraph builds a state machine with `fetch_data` → `parse_data` flow
   - Initial state includes musician name and era bounds

2. **Data Fetching**
   - Queries MusicBrainz API for artist relationships
   - Formats results as plain text
   - Falls back to mock data if API fails (for development)

3. **LLM Parsing**
   - Sends raw text + system prompt to LLM
   - Uses **structured output** with Pydantic validation
   - LLM extracts nodes (musicians) and edges (collaborations)
   - Filters by era, validates schema

4. **Graph Construction**
   - Converts validated JSON to NetworkX graph
   - Adds node attributes (instrument, role)
   - Adds edge attributes (collaboration type, weight)

5. **Metrics Computation**
   - Calculates centrality measures
   - Identifies key connectors in the network
   - Analyzes clustering patterns

6. **Visualization**
   - Generates interactive HTML with PyVis
   - Node size reflects importance (degree centrality)
   - Hover to see detailed metrics
   - Physics simulation for natural layout

---

## Data Source

**Primary**: [MusicBrainz API](https://musicbrainz.org) — Open music encyclopedia with rich relationship data

**Fallback**: Mock data for development/demonstration

The project is designed to easily swap data sources by modifying `agent/tools.py`.

---

## Key Learning Outcomes

This project demonstrates:

✅ **LangGraph state machines** for agent workflow control  
✅ **Structured LLM output** with Pydantic validation  
✅ **Tool integration** (API calls within agent context)  
✅ **LLM + deterministic code** separation (hybrid architecture)  
✅ **Error handling** throughout the pipeline  
✅ **NetworkX** for graph manipulation  
✅ **PyVis** for interactive visualization  

---

## Example Output

For **Charlie Parker (1940-1960)**:
- ~8-12 nodes (key bebop musicians)
- ~15-20 edges (collaboration relationships)
- Centrality highlights: Parker, Dizzy Gillespie, Miles Davis, Max Roach

**Open `data/output/jazz_graph.html` in your browser to explore!**

---

## Limitations & Future Work

**Current Limitations**:
- MusicBrainz API may have incomplete data for historical jazz musicians
- Mock fallback data is used for reliability during development
- Network size limited by API rate limits and LLM context window

**Future Enhancements**:
- Add web scraping for JazzDisco.org (more complete historical data)
- Implement caching to avoid redundant API calls
- Add CLI arguments for custom musicians/eras
- Export metrics to JSON for further analysis
- Support multiple seed musicians
- Add time-series analysis (collaboration evolution)

---

## Contributing

This is an educational project. Contributions welcome:
- Better data sources
- Improved error handling
- Additional SNA metrics
- UI improvements
- Test coverage

---

## License

MIT License — feel free to use for learning and experimentation.
