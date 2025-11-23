from typing import Dict
import networkx as nx


def compute_metrics(G: nx.Graph) -> Dict[str, Dict[str, float]]:
    """
    Compute a few standard SNA metrics on the graph.
    
    Args:
        G: NetworkX graph to analyze
        
    Returns:
        Dictionary containing degree centrality, betweenness centrality, and clustering metrics
        
    Raises:
        ValueError: If the graph is empty or invalid
    """
    try:
        if G is None:
            raise ValueError("Graph cannot be None")
            
        if G.number_of_nodes() == 0:
            print("Warning: Graph has no nodes. Returning empty metrics.")
            return {
                "degree_centrality": {},
                "betweenness_centrality": {},
                "clustering": {},
            }
        
        degree_centrality = nx.degree_centrality(G)
        betweenness_centrality = nx.betweenness_centrality(G, normalized=True)
        clustering = nx.clustering(G)

        return {
            "degree_centrality": degree_centrality,
            "betweenness_centrality": betweenness_centrality,
            "clustering": clustering,
        }
        
    except Exception as e:
        print(f"Error computing metrics: {e}")
        raise
