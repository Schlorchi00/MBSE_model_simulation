from src.core.network import DynamicNetwork
from src.simulation.engine import SimulationEngine
from src.models.function_registry import MODEL_FUNCTIONS
from src.config.config import BASE_DESIGNS, generate_weighting_scenarios
from src.reporting.summary import print_iteration_summary
from src.visualization.visualize_graph import visualize_network_graph, plot_domain_scores, plot_base_design_comparison, plot_weighting_impact
from src.reporting.pdf_report import generate_pdf_report

def run_scenario(config, model_functions, plot_hypergraph=True):
    """Helper function to set up and run a single simulation scenario."""
    scenario_name = config['name']
    print("==========================================================")
    print(f"RUNNING SCENARIO: {scenario_name}")
    
    network = DynamicNetwork()
    network.load_from_config(config)

    engine = SimulationEngine(network, model_functions)
    results = engine.run(scenario_name=scenario_name)
    
    safe_name = scenario_name.replace(' ', '_').replace('/', '_')
    
    # Only plot the hypergraph if requested (to avoid redundancy in the weighting study)
    if plot_hypergraph:
        visualize_network_graph(results['final_network'], safe_name)
        
    plot_domain_scores(results, safe_name)
    
    results['config'] = config
    
    return results

if __name__ == "__main__":
    # --- PART 1: Compare the three main design concepts with BALANCED weights ---
    print("\n\n--- STAGE 1: COMPARING BASE DESIGNS (BALANCED WEIGHTS) ---\n")
    base_design_results = []
    for base_design_config in BASE_DESIGNS:
        # Create the "Balanced" version for the base comparison
        balanced_config = generate_weighting_scenarios(base_design_config)[0]
        iteration_results = run_scenario(balanced_config, MODEL_FUNCTIONS, plot_hypergraph=True)
        base_design_results.append(iteration_results)
    
    # --- PART 2: Run uncertainty analysis on ALL base designs ---
    print("\n\n--- STAGE 2: UNCERTAINTY ANALYSIS (VARYING WEIGHTS) ---\n")
    weighting_study_results = []
    for base_design_config in BASE_DESIGNS:
        # Generate all 4 weighting variations for the current base design
        weighting_variations = generate_weighting_scenarios(base_design_config)
        
        for scenario_config in weighting_variations:
            # We don't need to plot the hypergraph again for these variations
            iteration_results = run_scenario(scenario_config, MODEL_FUNCTIONS, plot_hypergraph=False)
            weighting_study_results.append(iteration_results)
            
    # --- PART 3: Generate Final Report ---
    # Print a summary of all 12 runs to the console
    print_iteration_summary(weighting_study_results)
    
    # Create the plot for the initial base design comparison
    base_comparison_chart_path = "base_design_comparison_chart.png"
    plot_base_design_comparison(base_design_results, base_comparison_chart_path)
    
    # Create the plot for the weighting uncertainty study
    weighting_chart_path = "weighting_impact_summary.png"
    plot_weighting_impact(weighting_study_results, weighting_chart_path)
    
    # Generate the final PDF report with both sets of results
    generate_pdf_report(base_design_results, base_comparison_chart_path, weighting_study_results, weighting_chart_path)
