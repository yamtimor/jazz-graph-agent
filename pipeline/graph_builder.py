from typing import Dict, List, Any
import networkx as nx


def build_graph(graph_data: Dict[str, Any]) -> nx.Graph:
    """
    Build an undirected NetworkX graph from a JSON-like structure:

    {
      "nodes": [{"id": "John Coltrane", "instrument": "tenor sax"}, ...],
      "edges": [{"source": "John Coltrane", "target": "Miles Davis", "weight": 3}, ...]
    }
    """
    nodes: List[Dict[str, Any]] = graph_data.get("nodes", [])
    edges: List[Dict[str, Any]] = graph_data.get("edges", [])

    G = nx.Graph()

    for node in nodes:
        node_id = node["id"]
        attrs = {k: v for k, v in node.items() if k != "id"}
        G.add_node(node_id, **attrs)

    for edge in edges:
        source = edge["source"]
        target = edge["target"]
        attrs = {k: v for k, v in edge.items() if k not in ("source", "target")}
        G.add_edge(source, target, **attrs)

    return G
