def calculate_material_metrics(node):
    """Calculates all metrics for a material."""
    # Value Scores
    embodied_carbon = node.attributes.get('embodied_carbon', 100)
    sustainability_score = max(0, 1 - (embodied_carbon / 20.0))
    node.value_scores['sustainability'] = sustainability_score
    
    cost_per_kg = node.attributes.get('cost_per_kg', 50)
    cost_score = max(0, 1 - (cost_per_kg / 10.0))
    node.value_scores['cost'] = cost_score
    
    # Functionality Score
    stiffness = node.attributes.get('stiffness', 0)
    rigidity_score = min(1, stiffness / 250.0) # Normalize against a high stiffness value
    node.functionality_scores['structural_rigidity'] = rigidity_score
    
    print(f"  - Calculated internal metrics for '{node.id}': Rigidity={rigidity_score:.3f}, Sustainability={sustainability_score:.3f}, Cost={cost_score:.3f}")

def calculate_design_performance(node):
    """Calculates a performance score based on design simulation results."""
    fail_rate = node.attributes.get('stress_fail_rate', 1.0)
    performance_score = 1.0 - fail_rate
    node.functionality_scores['performance'] = performance_score
    print(f"  - Calculated internal performance for '{node.id}': {performance_score:.3f}")

def calculate_manufacturing_metrics(node):
    """Calculates sustainability for a manufacturing process."""
    energy = node.attributes.get('energy_consumption', 100)
    waste = node.attributes.get('waste_rate', 1.0)
    sustainability_score = max(0, 1 - ((energy / 50.0) + waste) / 2)
    node.value_scores['sustainability'] = sustainability_score
    print(f"  - Calculated internal sustainability for '{node.id}': {sustainability_score:.3f}")