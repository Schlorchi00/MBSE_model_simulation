# This file contains the scenario configurations for distinct design concepts.

SCENARIOS = [
    # --- Scenario A: High-Performance Baseline ---
    {
        'name': "A_CFRP_Honeycomb_Autoclave",
        'image_path': "src/data/thermoplast_sandwich.PNG", # Corrected path
        'nodes': [
            {'node_id': 'material_assessment', 'domain': 'Material', 'node_type': 'Assessment', 'attributes': {'face_sheet_modulus': 150, 'core_density': 0.05, 'cost_per_m2': 300, 'thermal_conductivity': 0.08, 'recyclability_score': 0.2}, 'function_path': 'models.system.material_assessment'},
            {'node_id': 'design_assembly', 'domain': 'Design', 'node_type': 'Assembly', 'attributes': {'adhesive_type': 'epoxy_film', 'fastener_count': 0, 'disassembly_ease': 0.1}, 'function_path': 'models.system.design_assembly'},
            {'node_id': 'technology_assessment', 'domain': 'Manufacturing', 'node_type': 'Assessment', 'attributes': {'energy_per_part': 60, 'scrap_rate': 0.1}, 'function_path': 'models.system.manufacturing_assessment'},
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
            {'type': 'functionality', 'source': 'material_assessment', 'target': 'design_prediction', 'label': 'thermal_resistance', 'weight': 1.0}
        ]
    },
    # --- Scenario B: Recyclable Thermoplastic ---
    {
        'name': "B_Thermoplastic_3D-Printed_Core",
        'image_path': "src/data/thermoplast_sandwich.PNG", # Corrected path
        'nodes': [
            {'node_id': 'material_assessment', 'domain': 'Material', 'node_type': 'Assessment', 'attributes': {'face_sheet_modulus': 110, 'core_density': 0.12, 'cost_per_m2': 220, 'thermal_conductivity': 0.15, 'recyclability_score': 0.9}, 'function_path': 'models.system.material_assessment'},
            {'node_id': 'design_assembly', 'domain': 'Design', 'node_type': 'Assembly', 'attributes': {'adhesive_type': 'thermal_bonding', 'fastener_count': 4, 'disassembly_ease': 0.8}, 'function_path': 'models.system.design_assembly'},
            {'node_id': 'technology_assessment', 'domain': 'Manufacturing', 'node_type': 'Assessment', 'attributes': {'energy_per_part': 40, 'scrap_rate': 0.05}, 'function_path': 'models.system.manufacturing_assessment'},
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
            {'type': 'functionality', 'source': 'material_assessment', 'target': 'design_prediction', 'label': 'thermal_resistance', 'weight': 1.0}
        ]
    },
    # --- Scenario C: Low-Cost Fiberglass ---
    {
        'name': "C_Fiberglass_Foam_Core",
        'image_path': "src/data/thermoplast_sandwich.PNG", # Corrected path
        'nodes': [
            {'node_id': 'material_assessment', 'domain': 'Material', 'node_type': 'Assessment', 'attributes': {'face_sheet_modulus': 70, 'core_density': 0.08, 'cost_per_m2': 100, 'thermal_conductivity': 0.04, 'recyclability_score': 0.1}, 'function_path': 'models.system.material_assessment'},
            {'node_id': 'design_assembly', 'domain': 'Design', 'node_type': 'Assembly', 'attributes': {'adhesive_type': 'epoxy_resin', 'fastener_count': 0, 'disassembly_ease': 0.1}, 'function_path': 'models.system.design_assembly'},
            {'node_id': 'technology_assessment', 'domain': 'Manufacturing', 'node_type': 'Assessment', 'attributes': {'energy_per_part': 25, 'scrap_rate': 0.18}, 'function_path': 'models.system.manufacturing_assessment'},
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
            {'type': 'functionality', 'source': 'material_assessment', 'target': 'design_prediction', 'label': 'thermal_resistance', 'weight': 1.0}
        ]
    }
]

# Add base models to each scenario to avoid repetition
BASE_NODES = [
    {'node_id': 'material_search', 'domain': 'Material', 'node_type': 'Search', 'attributes': {'target_face_sheet_modulus': 140}, 'function_path': 'models.system.material_search'},
    {'node_id': 'material_prediction', 'domain': 'Material', 'node_type': 'Prediction', 'attributes': {'simulated_delamination_risk': 0.1}, 'function_path': 'models.system.material_prediction'},
    {'node_id': 'design_creation', 'domain': 'Design', 'node_type': 'Creation', 'attributes': {'panel_thickness': 20, 'face_sheet_thickness': 1.0}, 'function_path': 'models.system.design_creation'},
    {'node_id': 'design_prediction', 'domain': 'Design', 'node_type': 'Prediction', 'attributes': {'max_deflection_mm': 0.5}, 'function_path': 'models.system.design_prediction'},
    {'node_id': 'technology_selection', 'domain': 'Manufacturing', 'node_type': 'Selection', 'attributes': {'process': 'autoclave_curing'}, 'function_path': 'models.system.technology_selection'},
    {'node_id': 'technology_simulation', 'domain': 'Manufacturing', 'node_type': 'Simulation', 'attributes': {'curing_time_hours': 4}, 'function_path': 'models.system.technology_simulation'}
]

for scenario in SCENARIOS:
    defined_nodes = {node['node_id'] for node in scenario['nodes']}
    for base_node in BASE_NODES:
        if base_node['node_id'] not in defined_nodes:
            scenario['nodes'].append(base_node)
