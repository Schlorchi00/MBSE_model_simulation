import copy
import random

# Base configuration for the sandwich panel
BASE_SCENARIO = {
    'name': "Sandwich Panel Iteration",
    'nodes': [
      # Material Domain
      {'node_id': 'material_search', 'domain': 'Material', 'node_type': 'Search', 'attributes': {'target_face_sheet_modulus': 140}, 'function_path': 'models.system.material_search'},
      {'node_id': 'material_assessment', 'domain': 'Material', 'node_type': 'Assessment', 'attributes': {'face_sheet_modulus': 150, 'face_sheet_density': 1.6, 'core_density': 0.05, 'core_shear_strength': 3.0, 'cost_per_m2': 300, 'thermal_conductivity': 0.08}, 'function_path': 'models.system.material_assessment'},
      {'node_id': 'material_prediction', 'domain': 'Material', 'node_type': 'Prediction', 'attributes': {'simulated_delamination_risk': 0.1}, 'function_path': 'models.system.material_prediction'},
      # Design Domain
      {'node_id': 'design_creation', 'domain': 'Design', 'node_type': 'Creation', 'attributes': {'panel_thickness': 20, 'face_sheet_thickness': 1.0}, 'function_path': 'models.system.design_creation'},
      {'node_id': 'design_assembly', 'domain': 'Design', 'node_type': 'Assembly', 'attributes': {'adhesive_type': 'epoxy_film'}, 'function_path': 'models.system.design_assembly'},
      {'node_id': 'design_prediction', 'domain': 'Design', 'node_type': 'Prediction', 'attributes': {'max_deflection_mm': 0.5}, 'function_path': 'models.system.design_prediction'},
      # Manufacturing Domain
      {'node_id': 'technology_selection', 'domain': 'Manufacturing', 'node_type': 'Selection', 'attributes': {'process': 'autoclave_curing'}, 'function_path': 'models.system.technology_selection'},
      {'node_id': 'technology_assessment', 'domain': 'Manufacturing', 'node_type': 'Assessment', 'attributes': {'energy_per_part': 60, 'scrap_rate': 0.1}, 'function_path': 'models.system.manufacturing_assessment'},
      {'node_id': 'technology_simulation', 'domain': 'Manufacturing', 'node_type': 'Simulation', 'attributes': {'curing_time_hours': 4}, 'function_path': 'models.system.technology_simulation'}
    ],
    'edges': [
      {'type': 'dependency', 'sources': ['design_creation'], 'target': 'material_search'},
      {'type': 'dependency', 'sources': ['material_search'], 'target': 'material_assessment'},
      {'type': 'dependency', 'sources': ['material_assessment', 'design_creation'], 'target': 'design_prediction'},
      {'type': 'dependency', 'sources': ['design_prediction'], 'target': 'material_prediction'},
      {'type': 'dependency', 'sources': ['material_assessment', 'design_creation'], 'target': 'technology_selection'},
      {'type': 'dependency', 'sources': ['technology_selection', 'design_assembly'], 'target': 'technology_assessment'},
      {'type': 'value', 'source': 'material_assessment', 'target': 'technology_assessment', 'label': 'total_cost', 'weight': 0.8},
      {'type': 'value', 'source': 'material_assessment', 'target': 'technology_assessment', 'label': 'sustainability', 'weight': 0.9},
      {'type': 'functionality', 'source': 'material_assessment', 'target': 'design_prediction', 'label': 'stiffness_to_weight', 'weight': 1.0},
      {'type': 'functionality', 'source': 'material_assessment', 'target': 'design_prediction', 'label': 'buckling_resistance', 'weight': 0.8},
      {'type': 'functionality', 'source': 'material_prediction', 'target': 'design_prediction', 'label': 'durability', 'weight': 0.7},
      # Added new functionality edge
      {'type': 'functionality', 'source': 'material_assessment', 'target': 'design_prediction', 'label': 'thermal_resistance', 'weight': 1.0}
    ]
}

def generate_scenarios(num_iterations=10):
    """
    Generates a list of scenarios with significant and non-linear variations
    to simulate a realistic design space exploration.
    """
    scenarios = []
    for i in range(num_iterations):
        new_scenario = copy.deepcopy(BASE_SCENARIO)
        new_scenario['name'] = f"Iteration {i + 1}"
        
        # Introduce more significant and varied changes for each iteration
        for node in new_scenario['nodes']:
            if node['node_id'] == 'material_assessment':
                # Cost increases but with random fluctuations and potential price shocks
                cost_fluctuation = random.uniform(-30, 30)
                price_shock = 50 if random.random() < 0.2 else 0 # 20% chance of a price shock
                node['attributes']['cost_per_m2'] = 300 + (i * 5) + cost_fluctuation + price_shock
                
                # Denser core is stronger but less sustainable, with non-linear progression
                core_density_increase = (i**1.2) * 0.005 # Non-linear increase
                node['attributes']['core_density'] = 0.04 + core_density_increase + random.uniform(-0.005, 0.005)
                node['attributes']['core_shear_strength'] = 2.8 + (core_density_increase * 50)
                
                # Thermal conductivity gets slightly worse with density
                node['attributes']['thermal_conductivity'] = 0.07 + core_density_increase * random.uniform(0.8, 1.2)
            
            if node['node_id'] == 'design_creation':
                # Panel thickness varies more widely, not strictly increasing
                node['attributes']['panel_thickness'] = 20 + random.uniform(-3, 5)

            if node['node_id'] == 'design_prediction':
                # Deflection is a function of panel thickness (thicker is better) plus a random factor
                thickness = next(n['attributes']['panel_thickness'] for n in new_scenario['nodes'] if n['node_id'] == 'design_creation')
                node['attributes']['max_deflection_mm'] = 1.5 - (thickness / 20.0) + random.uniform(-0.1, 0.1)

            if node['node_id'] == 'technology_assessment':
                # Scrap rate improves but with random setbacks (e.g., bad batch)
                scrap_improvement = i * 0.01
                scrap_setback = random.uniform(0, 0.05) if random.random() < 0.3 else 0 # 30% chance of a process issue
                node['attributes']['scrap_rate'] = max(0.02, 0.15 - scrap_improvement + scrap_setback)
                
                # Energy consumption varies randomly per batch
                node['attributes']['energy_per_part'] = random.uniform(45, 80)

        scenarios.append(new_scenario)
    return scenarios

SCENARIOS = generate_scenarios(10)