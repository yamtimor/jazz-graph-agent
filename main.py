from config import CONFIG
from agent.agent import run_jazz_agent
from pipeline.graph_builder import build_graph_from_json
from pipeline.metrics import compute_metrics
from pipeline.visualize import build_pyvis_html


def main():
    graph_json = run_jazz_agent()

    G = build_graph_from_json(graph_json)

    metrics = compute_metrics(G)

    build_pyvis_html(
        G,
        output_path=CONFIG.output_html_path,
        metrics=metrics,
    )


if __name__ == "__main__":
    main()
