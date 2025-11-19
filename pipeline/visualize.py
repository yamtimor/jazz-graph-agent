from pathlib import Path
from typing import Dict
import networkx as nx
from pyvis.network import Network

OUTPUT_DIR = Path("data/output")


def visualize_graph(
    G: nx.Graph,
    metrics: Dict[str, Dict[str, float]],
    filename: str = "jazz_graph.html",
) -> Path:
    """
    Build an interactive PyVis visualization and save it under data/output/.
    Node size is based on degree centrality; tooltip shows basic metrics.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    net = Network(
        height="750px",
        width="100%",
        notebook=False,
        bgcolor="#111111",
        font_color="#EEEEEE",
    )
    net.barnes_hut()

    degree = metrics.get("degree_centrality", {})
    betweenness = metrics.get("betweenness_centrality", {})

    for node, attrs in G.nodes(data=True):
        d = degree.get(node, 0.0)
        b = betweenness.get(node, 0.0)

        size = 10 + d * 40

        title_lines = [
            f"<b>{node}</b>",
            f"Degree centrality: {d:.3f}",
            f"Betweenness: {b:.3f}",
        ]
        label = attrs.get("label", node)

        net.add_node(
            node,
            label=label,
            value=size,
            title="<br>".join(title_lines),
        )

    for u, v, attrs in G.edges(data=True):
        net.add_edge(u, v)

    out_path = OUTPUT_DIR / filename
    net.show(out_path.as_posix())
    return out_path
