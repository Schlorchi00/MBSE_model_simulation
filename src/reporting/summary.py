def print_iteration_summary(all_results):
    """
    Prints a summary report comparing all simulation iterations and announces the best one.
    """
    print("==========================================================")
    print("           COMPLETE SIMULATION ITERATION REPORT           ")
    print("==========================================================")

    best_iteration = None
    best_score = -1

    for i, result in enumerate(all_results):
        scenario_name = result['scenario_name']
        meta_score = result['meta_score']
        
        if meta_score > best_score:
            best_score = meta_score
            best_iteration = scenario_name

        print(f"\n--- ITERATION {i+1}: {scenario_name} ---")
        print(f"  Meta Score: {meta_score:.4f}")
        
        print("\n  Node Details:")
        for node_id, state in sorted(result['node_states'].items()):
            print(f"    - Node: {node_id}")
            if state['attributes']:
                print(f"      Input Attributes: {state['attributes']}")
            
            all_scores = {**state['final_functionality_scores'], **state['final_value_scores']}
            if all_scores:
                score_str = ", ".join([f"{k}: {v:.3f}" for k, v in sorted(all_scores.items())])
                print(f"      Final Scores: {score_str}")

    print("\n==========================================================")
    print(f"🏆 Best Performing Iteration: '{best_iteration}' with a Meta Score of {best_score:.4f}")
    print("==========================================================")