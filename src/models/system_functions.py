# --- Material Domain Functions ---
def material_search(node):
    modulus = node.attributes.get('target_face_sheet_modulus', 0)
    node.functionality_scores['performance'] = max(0, 1 - (modulus / 500.0))
    node.value_scores['total_cost'] = 0.95
    node.value_scores['sustainability'] = 0.5
    print(f"  - Executed material_search for '{node.id}'")

def material_assessment(node):
    # Value
    cost = node.attributes.get('cost_per_m2', 1000)
    node.value_scores['total_cost'] = max(0, 1 - (cost / 500.0))
    # Sustainability now includes recyclability
    core_density = node.attributes.get('core_density', 1)
    recyclability = node.attributes.get('recyclability_score', 0)
    node.value_scores['sustainability'] = ((max(0, 1 - (core_density / 0.1))) + recyclability) / 2
    
    # --- FIX: Changed score name for consistency ---
    face_modulus = node.attributes.get('face_sheet_modulus', 0)
    node.functionality_scores['structural_rigidity'] = min(1.0, face_modulus / 180.0) # Normalize against a high modulus value
    
    conductivity = node.attributes.get('thermal_conductivity', 1)
    node.functionality_scores['thermal_resistance'] = max(0, 1 - (conductivity / 0.2))
    print(f"  - Executed material_assessment for '{node.id}'")

def material_prediction(node):
    delamination_risk = node.attributes.get('simulated_delamination_risk', 1.0)
    node.functionality_scores['performance'] = 1.0 - delamination_risk
    node.value_scores['total_cost'] = 1.0
    node.value_scores['sustainability'] = 1.0
    print(f"  - Executed material_prediction for '{node.id}'")

# ... (rest of the functions are the same)
def design_creation(node):
    thickness = node.attributes.get('panel_thickness', 0)
    node.functionality_scores['performance'] = min(1, thickness / 25.0)
    node.value_scores['total_cost'] = max(0, 1 - (thickness / 50.0))
    node.value_scores['sustainability'] = max(0, 1 - (thickness / 50.0))
    print(f"  - Executed design_creation for '{node.id}'")

def design_assembly(node):
    ease = node.attributes.get('disassembly_ease', 0)
    node.value_scores['sustainability'] = ease
    node.functionality_scores['performance'] = 0.9
    node.value_scores['total_cost'] = 0.9
    print(f"  - Executed design_assembly for '{node.id}'")

def design_prediction(node):
    deflection = node.attributes.get('max_deflection_mm', 10)
    node.functionality_scores['performance'] = max(0, 1 - (deflection / 2.0))
    node.value_scores['total_cost'] = 1.0
    node.value_scores['sustainability'] = 1.0
    print(f"  - Executed design_prediction for '{node.id}'")

def technology_selection(node):
    process = node.attributes.get('process', 'hand_layup')
    node.functionality_scores['performance'] = 0.9 if process == 'autoclave_curing' else 0.6
    node.value_scores['total_cost'] = 0.6 if process == 'autoclave_curing' else 0.8
    node.value_scores['sustainability'] = 0.5
    print(f"  - Executed technology_selection for '{node.id}'")

def manufacturing_assessment(node):
    energy = node.attributes.get('energy_per_part', 100)
    scrap = node.attributes.get('scrap_rate', 1.0)
    node.value_scores['sustainability'] = max(0, 1 - ((energy / 100.0) + scrap) / 2)
    node.value_scores['total_cost'] = max(0, 1 - ((energy / 150.0) + scrap) / 2)
    node.functionality_scores['performance'] = 1.0
    print(f"  - Executed manufacturing_assessment for '{node.id}'")

def technology_simulation(node):
    curing_time = node.attributes.get('curing_time_hours', 8)
    node.value_scores['total_cost'] = max(0, 1 - (curing_time / 12.0))
    node.functionality_scores['performance'] = max(0, 1 - (curing_time / 24.0))
    node.value_scores['sustainability'] = max(0, 1 - (curing_time / 12.0))
    print(f"  - Executed technology_simulation for '{node.id}'")