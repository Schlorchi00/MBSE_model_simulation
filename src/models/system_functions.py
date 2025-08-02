# --- Material Domain Functions ---
def material_search(node):
    """Placeholder for a material database search."""
    modulus = node.attributes.get('target_face_sheet_modulus', 0)
    # Performance: Higher modulus is harder to find.
    node.functionality_scores['performance'] = max(0, 1 - (modulus / 500.0))
    # Cost: Simple search has low cost impact.
    node.value_scores['total_cost'] = 0.95
    # Sustainability: Assume search has neutral sustainability impact.
    node.value_scores['sustainability'] = 0.5
    print(f"  - Executed material_search for '{node.id}'")

def material_assessment(node):
    """Calculates metrics for sandwich panel materials."""
    # Value
    cost = node.attributes.get('cost_per_m2', 1000)
    node.value_scores['total_cost'] = max(0, 1 - (cost / 500.0))
    # Sustainability
    core_density = node.attributes.get('core_density', 1)
    node.value_scores['sustainability'] = max(0, 1 - (core_density / 0.1))
    
    # Functionality
    face_modulus = node.attributes.get('face_sheet_modulus', 0)
    stiffness_to_weight = face_modulus / (core_density * 1000)
    node.functionality_scores['stiffness_to_weight'] = min(1.0, stiffness_to_weight / 2.0)
    conductivity = node.attributes.get('thermal_conductivity', 1)
    node.functionality_scores['thermal_resistance'] = max(0, 1 - (conductivity / 0.2))
    print(f"  - Executed material_assessment for '{node.id}'")

def material_prediction(node):
    """Placeholder for material performance simulation."""
    delamination_risk = node.attributes.get('simulated_delamination_risk', 1.0)
    # Performance: Lower risk is better.
    node.functionality_scores['performance'] = 1.0 - delamination_risk
    node.value_scores['total_cost'] = 1.0 # No direct cost
    node.value_scores['sustainability'] = 1.0 # No direct impact
    print(f"  - Executed material_prediction for '{node.id}'")

# --- Design Domain Functions ---
def design_creation(node):
    """Calculates scores based on the initial design concept."""
    thickness = node.attributes.get('panel_thickness', 0)
    # Performance: Thicker is generally stronger.
    node.functionality_scores['performance'] = min(1, thickness / 25.0)
    # Cost: Thicker uses more material.
    node.value_scores['total_cost'] = max(0, 1 - (thickness / 50.0))
    # Sustainability: More material is less sustainable.
    node.value_scores['sustainability'] = max(0, 1 - (thickness / 50.0))
    print(f"  - Executed design_creation for '{node.id}'")

def design_assembly(node):
    """Calculates scores based on assembly complexity."""
    adhesive = node.attributes.get('adhesive_type', 'none')
    # Sustainability: Certain adhesives are better than others.
    node.value_scores['sustainability'] = 0.8 if adhesive == 'epoxy_film' else 0.4
    # Performance: Assumed high.
    node.functionality_scores['performance'] = 0.9
    # Cost: Assumed high (good).
    node.value_scores['total_cost'] = 0.9
    print(f"  - Executed design_assembly for '{node.id}'")

def design_prediction(node):
    """Calculates a performance score based on design simulation results."""
    deflection = node.attributes.get('max_deflection_mm', 10)
    # Performance: Lower deflection is better.
    node.functionality_scores['performance'] = max(0, 1 - (deflection / 2.0))
    node.value_scores['total_cost'] = 1.0 # No direct cost
    node.value_scores['sustainability'] = 1.0 # No direct impact
    print(f"  - Executed design_prediction for '{node.id}'")

# --- Manufacturing Domain Functions ---
def technology_selection(node):
    """Placeholder for selecting a manufacturing technology."""
    process = node.attributes.get('process', 'hand_layup')
    # Performance: Confidence in the selected process.
    node.functionality_scores['performance'] = 0.9 if process == 'autoclave_curing' else 0.6
    # Cost: Autoclave has high initial cost.
    node.value_scores['total_cost'] = 0.6 if process == 'autoclave_curing' else 0.8
    # Sustainability: No direct impact.
    node.value_scores['sustainability'] = 0.5
    print(f"  - Executed technology_selection for '{node.id}'")

def manufacturing_assessment(node):
    """Calculates sustainability and cost for a manufacturing process."""
    energy = node.attributes.get('energy_per_part', 100)
    scrap = node.attributes.get('scrap_rate', 1.0)
    # Sustainability
    node.value_scores['sustainability'] = max(0, 1 - ((energy / 100.0) + scrap) / 2)
    # Cost: Energy and scrap drive cost.
    node.value_scores['total_cost'] = max(0, 1 - ((energy / 150.0) + scrap) / 2)
    # Performance: No direct impact.
    node.functionality_scores['performance'] = 1.0
    print(f"  - Executed manufacturing_assessment for '{node.id}'")

def technology_simulation(node):
    """Placeholder for simulating the manufacturing process."""
    curing_time = node.attributes.get('curing_time_hours', 8)
    # Cost: Faster is cheaper.
    node.value_scores['total_cost'] = max(0, 1 - (curing_time / 12.0))
    # Performance: Faster might reduce quality.
    node.functionality_scores['performance'] = max(0, 1 - (curing_time / 24.0))
    # Sustainability: Faster is more energy efficient.
    node.value_scores['sustainability'] = max(0, 1 - (curing_time / 12.0))
    print(f"  - Executed technology_simulation for '{node.id}'")
