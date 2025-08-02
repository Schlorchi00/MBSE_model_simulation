def print_value_propagation(network):
    """Prints the history of all value scores for each node."""
    print("\n--- Value Score Propagation History ---")
    for node_id, node in network.nodes.items():
        print(f"[{node.id.ljust(25)}]")
        all_labels = set()
        for history_point in node.value_score_history:
            all_labels.update(history_point.keys())
        
        if not all_labels:
            continue
            
        for label in sorted(list(all_labels)):
            history_str = " -> ".join([f"{s.get(label, 0.0):.3f}" for s in node.value_score_history])
            print(f"  {label.ljust(15)}: {history_str}")