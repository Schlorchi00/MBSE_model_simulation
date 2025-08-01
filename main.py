from src.core.network import DynamicNetwork
from src.simulation.engine import SimulationEngine
from src.models.function_registry import MODEL_FUNCTIONS
from src.config.config import SCENARIOS
from src.reporting.summary import print_iteration_summary
from src.visualization.visualize_graph import visualize_network_graph, plot_domain_scores, plot_summary_graph

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
    
    visualize_network_graph(results['final_network'], scenario_name)
    plot_domain_scores(results, scenario_name)
    
    return results

if __name__ == "__main__":
    all_results = []
    for scenario_config in SCENARIOS:
        iteration_results = run_scenario(scenario_config, MODEL_FUNCTIONS)
        all_results.append(iteration_results)
    
    # Print the text summary and generate the final summary plot
    print_iteration_summary(all_results)
    plot_summary_graph(all_results)