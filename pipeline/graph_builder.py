from typing import Dict, List, Any
import networkx as nx


def build_graph_from_json(graph_data: Dict[str, Any]) -> nx.Graph:
    """
    Build an undirected NetworkX graph from a JSON-like structure:

    {
      "nodes": [{"id": "John Coltrane", "instrument": "tenor sax"}, ...],
      "edges": [{"source": "John Coltrane", "target": "Miles Davis", "weight": 3}, ...]
    }
    
    Raises:
        ValueError: If graph_data is invalid or missing required fields
        KeyError: If nodes or edges are missing required keys
    """
    try:
        if not isinstance(graph_data, dict):
            raise ValueError(f"graph_data must be a dictionary, got {type(graph_data)}")
        
        nodes: List[Dict[str, Any]] = graph_data.get("nodes", [])
        edges: List[Dict[str, Any]] = graph_data.get("edges", [])
        
        if not isinstance(nodes, list):
            raise ValueError(f"'nodes' must be a list, got {type(nodes)}")
        if not isinstance(edges, list):
            raise ValueError(f"'edges' must be a list, got {type(edges)}")

        G = nx.Graph()

        for idx, node in enumerate(nodes):
            try:
                node_id = node["id"]
                attrs = {k: v for k, v in node.items() if k != "id"}
                G.add_node(node_id, **attrs)
            except KeyError as e:
                raise KeyError(f"Node at index {idx} is missing required key: {e}")
            except Exception as e:
                raise ValueError(f"Error processing node at index {idx}: {e}")

        for idx, edge in enumerate(edges):
            try:
                source = edge["source"]
                target = edge["target"]
                attrs = {k: v for k, v in edge.items() if k not in ("source", "target")}
                G.add_edge(source, target, **attrs)
            except KeyError as e:
                raise KeyError(f"Edge at index {idx} is missing required key: {e}")
            except Exception as e:
                raise ValueError(f"Error processing edge at index {idx}: {e}")

        return G
        
    except Exception as e:
        print(f"Error building graph: {e}")
        raise
