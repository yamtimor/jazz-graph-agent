# jazz-graph-agent

A minimal, end-to-end LangChain agent that fetches jazz data, extracts relationships between musicians, and builds a social graph with SNA metrics and interactive visualization.

This project focuses on the bebop era, but the architecture supports any jazz domain.

---

## Project Overview

`jazz-graph-agent` is a tiny, educational, first-agent project designed to demonstrate:

- how to build a simple LangChain agent  
- how to let the agent fetch + parse real-world jazz data  
- how to transform that output into a NetworkX graph  
- how to compute basic Social Network Analysis (SNA) metrics  
- how to produce a PyVis interactive graph  

The entire pipeline is intentionally lightweight, easy to understand, and runnable locally.

---

## Architecture

### 1. LangChain Agent (LLM-driven)

A single agent orchestrates two tools:

1. `fetch_jazz_data(query)`  
   Fetches raw musician/collaboration information from https://www.jazzdisco.org/

2. `parse_jazz_data(raw_text)`  
   Uses the LLM to convert raw text into a JSON graph structure:

{
  "nodes": [...],
  "edges": [...]
}

The agent handles all messy logic — fetching, parsing, relationship extraction.

---

### 2. Application Layer (deterministic Python)

Once the agent outputs structured data, deterministic Python code:

- builds a NetworkX graph  
- computes:
  - degree centrality  
  - betweenness centrality  
  - clustering coefficient  
- generates an interactive PyVis HTML visualization  
- saves everything to `data/output/`

No LLMs are used in this phase.

---

## Folder Structure

jazz-graph-agent/
|
├── main.py
├── agent/
│   ├── tools.py
│   ├── agent.py
|
├── pipeline/
│   ├── graph_builder.py
│   ├── metrics.py
│   ├── visualize.py
|
└── data/output/

---

## Data Source

This project uses JazzDisco — one of the most complete discography resources for jazz:

https://www.jazzdisco.org/

This site is ideal for extracting collaboration networks because it includes detailed session participation.

---

## Goals of This Project

- Build a simple, real LangChain agent  
- Demonstrate tool-calling  
- Learn agent orchestration end-to-end  
- Keep everything compact and beginner-friendly  

---

## Status

Under active development.  
This PR focuses on project scaffolding and documentation.
