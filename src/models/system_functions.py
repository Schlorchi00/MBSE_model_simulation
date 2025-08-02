# --- Material Domain Functions ---
def material_search(node):
    """Placeholder for a material database search."""
    modulus = node.attributes.get('target_face_sheet_modulus', 0)
    node.functionality_scores['search_feasibility'] = max(0, 1 - (modulus / 500.0))
    print(f"  - Executed material_search for '{node.id}'")

def material_assessment(node):
    """Calculates metrics for sandwich panel materials."""
    # Value scores
    cost = node.attributes.get('cost_per_m2', 1000)
    node.value_scores['total_cost'] = max(0, 1 - (cost / 500.0))
    
    # Functionality scores
    face_modulus = node.attributes.get('face_sheet_modulus', 0)
    core_density = node.attributes.get('core_density', 1)
    stiffness_to_weight = face_modulus / (core_density * 1000) # Simplified ratio
    node.functionality_scores['stiffness_to_weight'] = min(1.0, stiffness_to_weight / 2.0)

    core_strength = node.attributes.get('core_shear_strength', 0)
    node.functionality_scores['buckling_resistance'] = min(1.0, core_strength / 5.0)
    print(f"  - Executed material_assessment for '{node.id}'")

def material_prediction(node):
    """Placeholder for material performance simulation."""
    delamination_risk = node.attributes.get('simulated_delamination_risk', 1.0)
    node.functionality_scores['durability'] = 1.0 - delamination_risk
    print(f"  - Executed material_prediction for '{node.id}'")

# --- Design Domain Functions ---
def design_creation(node):
    """Calculates scores based on the initial design concept."""
    thickness = node.attributes.get('panel_thickness', 0)
    # Thicker panels are generally more rigid but less 'elegant' or 'innovative'.
    node.functionality_scores['innovativeness'] = max(0, 1 - (thickness / 50.0))
    print(f"  - Executed design_creation for '{node.id}'")

def design_assembly(node):
    """Calculates scores based on assembly complexity."""
    # In this case, the adhesive choice could impact sustainability.
    adhesive = node.attributes.get('adhesive_type', 'none')
    sustainability_score = 0.8 if adhesive == 'epoxy_film' else 0.4
    node.value_scores['sustainability'] = sustainability_score
    print(f"  - Executed design_assembly for '{node.id}'")

def design_prediction(node):
    """Calculates a performance score based on design simulation results."""
    deflection = node.attributes.get('max_deflection_mm', 10)
    # Lower deflection is better performance.
    node.functionality_scores['performance'] = max(0, 1 - (deflection / 2.0))
    print(f"  - Executed design_prediction for '{node.id}'")

# --- Manufacturing Domain Functions ---
def technology_selection(node):
    """Placeholder for selecting a manufacturing technology."""
    process = node.attributes.get('process', 'hand_layup')
    # Autoclave is a high-confidence process.
    confidence = 0.9 if process == 'autoclave_curing' else 0.6
    node.functionality_scores['selection_confidence'] = confidence
    print(f"  - Executed technology_selection for '{node.id}'")

def manufacturing_assessment(node):
    """Calculates sustainability and cost for a manufacturing process."""
    energy = node.attributes.get('energy_per_part', 100)
    scrap = node.attributes.get('scrap_rate', 1.0)
    node.value_scores['sustainability'] = max(0, 1 - ((energy / 100.0) + scrap) / 2)
    print(f"  - Executed manufacturing_assessment for '{node.id}'")

def technology_simulation(node):
    """Placeholder for simulating the manufacturing process."""
    curing_time = node.attributes.get('curing_time_hours', 8)
    # Faster curing time is better for cost.
    node.value_scores['total_cost'] = max(0, 1 - (curing_time / 12.0))
    node.functionality_scores['manufacturability'] = max(0, 1 - (curing_time / 12.0))
    print(f"  - Executed technology_simulation for '{node.id}'")