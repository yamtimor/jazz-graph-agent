import sys
from config import CONFIG
from agent.agent import run_jazz_agent
from pipeline.graph_builder import build_graph_from_json
from pipeline.metrics import compute_metrics
from pipeline.visualize import build_pyvis_html


def main():
    """
    Main entry point for the jazz-graph-agent application.
    
    Orchestrates the complete pipeline:
    1. Run agent to fetch and parse jazz data
    2. Build NetworkX graph from structured data
    3. Compute social network analysis metrics
    4. Generate interactive visualization
    """
    try:
        print("Starting Jazz Graph Agent pipeline...\n")
        
        # Step 1: Run the agent
        print("Step 1: Running agent to extract collaboration data...")
        graph_json = run_jazz_agent()
        
        # Step 2: Build graph
        print("\nStep 2: Building NetworkX graph...")
        G = build_graph_from_json(graph_json)
        print(f"Graph built with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
        
        # Step 3: Compute metrics
        print("\nStep 3: Computing social network metrics...")
        metrics = compute_metrics(G)
        print("Metrics computed successfully")
        
        # Step 4: Visualize
        print("\nStep 4: Creating interactive visualization...")
        output_path = build_pyvis_html(
            G,
            output_path=CONFIG.output_html_path,
            metrics=metrics,
        )
        
        print(f"\n✓ Pipeline completed successfully!")
        print(f"✓ Visualization available at: {output_path}")
        print(f"\nOpen the file in a web browser to explore the jazz collaboration network.")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\nPipeline interrupted by user.")
        return 1
        
    except Exception as e:
        print(f"\n✗ Pipeline failed with error: {e}")
        print(f"\nFor more details, check the error messages above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
