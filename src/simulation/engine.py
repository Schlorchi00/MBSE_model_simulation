import collections

class SimulationEngine:
    def __init__(self, network, model_functions):
        self.network = network
        self.model_functions = model_functions

    def run(self, scenario_name, iterations=10, alpha=0.5, beta=0.5):
        """
        Main simulation loop. Now accepts scenario_name for reporting.
        """
        print("--- Starting Simulation ---")
        print("Step 1: Calculating initial internal scores...")
        for node in self.network.nodes.values():
            if node.function_path and node.function_path in self.model_functions:
                self.model_functions[node.function_path](node)

        print("\nStep 2: Running score propagation...")
        for i in range(iterations):
            self._propagate_scores(alpha, beta)
        print("  - Propagation complete.")

        meta_score = self._calculate_meta_score()
        print("--- Simulation Finished ---")
        
        results = {
            "scenario_name": scenario_name, # Pass the name through
            "meta_score": meta_score,
            "final_network": self.network,
            "node_states": {
                node.id: {
                    "attributes": node.attributes,
                    "final_value_scores": node.value_scores,
                    "final_functionality_scores": node.functionality_scores
                } for node in self.network.nodes.values()
            }
        }
        return results

    def _propagate_scores(self, alpha, beta):
        last_f_scores = {nid: n.functionality_scores.copy() for nid, n in self.network.nodes.items()}
        last_v_scores = {nid: n.value_scores.copy() for nid, n in self.network.nodes.items()}

        next_f_scores = {nid: n.functionality_scores.copy() for nid, n in self.network.nodes.items()}
        next_v_scores = {nid: n.value_scores.copy() for nid, n in self.network.nodes.items()}

        for node_id, node in self.network.nodes.items():
            propagated = collections.defaultdict(float)
            for edge in self.network.functionality_edges:
                if edge.target == node_id:
                    parent_score = last_f_scores.get(edge.source, {}).get(edge.label, 0.0)
                    propagated[edge.label] += edge.weight * parent_score
            for label, prop_score in propagated.items():
                internal = last_f_scores[node_id].get(label, 0.0)
                next_f_scores[node_id][label] = (alpha * internal) + ((1 - alpha) * prop_score)

        for node_id, node in self.network.nodes.items():
            propagated = collections.defaultdict(float)
            for edge in self.network.value_edges:
                 if edge.target == node_id:
                    parent_score = last_v_scores.get(edge.source, {}).get(edge.label, 0.0)
                    propagated[edge.label] += edge.weight * parent_score
            for label, prop_score in propagated.items():
                internal = last_v_scores[node_id].get(label, 0.0)
                next_v_scores[node_id][label] = (beta * internal) + ((1 - beta) * prop_score)
        
        for node_id, node in self.network.nodes.items():
            node.functionality_scores = next_f_scores[node_id]
            node.value_scores = next_v_scores[node_id]

    def _calculate_meta_score(self, weights=None):
        if weights is None:
            weights = {
                'technology_assessment': {'sustainability': 0.5, 'cost': 0.3},
                'design_prediction': {'performance': 0.8, 'structural_rigidity': 0.6}
            }
        meta_score = 0
        print("\nStep 3: Calculating final meta-score...")
        for node_id, value_weights in weights.items():
            node = self.network.get_node(node_id)
            if node:
                all_scores = {**node.functionality_scores, **node.value_scores}
                for value_label, weight in value_weights.items():
                    score = all_scores.get(value_label, 0.0)
                    meta_score += weight * score
                    print(f"  - {node_id} '{value_label}' score: {score:.4f} (weight: {weight})")
        return meta_score