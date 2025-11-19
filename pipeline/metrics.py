from typing import Dict
import networkx as nx


def compute_basic_metrics(G: nx.Graph) -> Dict[str, Dict[str, float]]:
    """
    Compute a few standard SNA metrics on the graph.
    """
    degree_centrality = nx.degree_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G, normalized=True)
    clustering = nx.clustering(G)

    return {
        "degree_centrality": degree_centrality,
        "betweenness_centrality": betweenness_centrality,
        "clustering": clustering,
    }
