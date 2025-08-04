from src.core.network import DynamicNetwork
from src.simulation.engine import SimulationEngine
from src.models.function_registry import MODEL_FUNCTIONS
from src.config.config import SCENARIOS
from src.reporting.summary import print_iteration_summary
from src.visualization.visualize_graph import visualize_network_graph, plot_domain_scores, plot_summary_graph
from src.reporting.pdf_report import generate_pdf_report

def run_scenario(config, model_functions):
    """Helper function to set up and run a single simulation scenario."""
    scenario_name = config['name']
    print("==========================================================")
    print(f"RUNNING SCENARIO: {scenario_name}")
    print("==========================================================")
    
    network = DynamicNetwork()
    network.load_from_config(config)

    engine = SimulationEngine(network, model_functions)
    results = engine.run(scenario_name=scenario_name)

    print(f"\nFINAL META-SCORE: {results['meta_score']:.4f}")
    
    # Sanitize scenario name for filenames
    safe_name = scenario_name.replace(' ', '_').replace('/', '_')
    visualize_network_graph(results['final_network'], safe_name)
    plot_domain_scores(results, safe_name)
    
    # --- FIX: Add the original config to the results package ---
    # This makes the image_path available to the PDF report generator.
    results['config'] = config
    
    return results

if __name__ == "__main__":
    all_results = []
    for scenario_config in SCENARIOS:
        iteration_results = run_scenario(scenario_config, MODEL_FUNCTIONS)
        all_results.append(iteration_results)
    
    # Print the text summary and generate the final summary plot
    print_iteration_summary(all_results)
    summary_chart_path = "final_summary_chart.png"
    plot_summary_graph(all_results, summary_chart_path)
    
    # Generate the final PDF report
    generate_pdf_report(all_results, summary_chart_path)