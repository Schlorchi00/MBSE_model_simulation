def print_iteration_summary(all_results):
    """
    Prints a summary report comparing the results of all simulation iterations.
    """
    print("==========================================================")
    print("           COMPLETE SIMULATION ITERATION REPORT           ")
    print("==========================================================")

    for i, result in enumerate(all_results):
        # The scenario name is now correctly passed in the results dictionary
        print(f"\n--- ITERATION {i+1}: {result['scenario_name']} ---")
        print(f"  Meta Score: {result['meta_score']:.4f}")
        
        print("\n  Node Details:")
        for node_id, state in result['node_states'].items():
            print(f"    - Node: {node_id}")
            if state['attributes']:
                print(f"      Input Attributes: {state['attributes']}")
            
            all_scores = {**state['final_functionality_scores'], **state['final_value_scores']}
            if all_scores:
                score_str = ", ".join([f"{k}: {v:.3f}" for k, v in sorted(all_scores.items())])
                print(f"      Final Scores: {score_str}")

    print("\n==========================================================")