# This file contains the scenario configuration for a sandwich panel.

SCENARIOS = [
  {
    'name': "Sandwich Panel Design (CFRP-Honeycomb)",
    'nodes': [
      # --- Material Domain ---
      {'node_id': 'material_search', 'domain': 'Material', 'node_type': 'Search', 'attributes': {'target_face_sheet_modulus': 140, 'target_core_shear_strength': 2.5}, 'function_path': 'models.system.material_search'},
      {'node_id': 'material_assessment', 'domain': 'Material', 'node_type': 'Assessment', 'attributes': {'face_sheet_modulus': 150, 'face_sheet_density': 1.6, 'core_density': 0.05, 'core_shear_strength': 3.0, 'cost_per_m2': 300}, 'function_path': 'models.system.material_assessment'},
      {'node_id': 'material_prediction', 'domain': 'Material', 'node_type': 'Prediction', 'attributes': {'simulated_delamination_risk': 0.1}, 'function_path': 'models.system.material_prediction'},

      # --- Design Domain ---
      {'node_id': 'design_creation', 'domain': 'Design', 'node_type': 'Creation', 'attributes': {'panel_thickness': 20, 'face_sheet_thickness': 1.0}, 'function_path': 'models.system.design_creation'},
      {'node_id': 'design_assembly', 'domain': 'Design', 'node_type': 'Assembly', 'attributes': {'adhesive_type': 'epoxy_film'}, 'function_path': 'models.system.design_assembly'},
      {'node_id': 'design_prediction', 'domain': 'Design', 'node_type': 'Prediction', 'attributes': {'max_deflection_mm': 0.5}, 'function_path': 'models.system.design_prediction'},

      # --- Manufacturing Domain ---
      {'node_id': 'technology_selection', 'domain': 'Manufacturing', 'node_type': 'Selection', 'attributes': {'process': 'autoclave_curing'}, 'function_path': 'models.system.technology_selection'},
      {'node_id': 'technology_assessment', 'domain': 'Manufacturing', 'node_type': 'Assessment', 'attributes': {'energy_per_part': 60, 'scrap_rate': 0.1}, 'function_path': 'models.system.manufacturing_assessment'},
      {'node_id': 'technology_simulation', 'domain': 'Manufacturing', 'node_type': 'Simulation', 'attributes': {'curing_time_hours': 4}, 'function_path': 'models.system.technology_simulation'}
    ],
    'edges': [
      # === Dependency Hyperedges (Workflow) ===
      {'type': 'dependency', 'sources': ['design_creation'], 'target': 'material_search'},
      {'type': 'dependency', 'sources': ['material_search'], 'target': 'material_assessment'},
      {'type': 'dependency', 'sources': ['material_assessment', 'design_creation'], 'target': 'design_prediction'},
      {'type': 'dependency', 'sources': ['design_prediction'], 'target': 'material_prediction'},
      {'type': 'dependency', 'sources': ['material_assessment', 'design_creation'], 'target': 'technology_selection'},
      {'type': 'dependency', 'sources': ['technology_selection', 'design_assembly'], 'target': 'technology_assessment'},
      
      # === Value Edges ===
      {'type': 'value', 'source': 'material_assessment', 'target': 'technology_assessment', 'label': 'total_cost', 'weight': 0.8},
      {'type': 'value', 'source': 'material_assessment', 'target': 'technology_assessment', 'label': 'sustainability', 'weight': 0.9},

      # === Functionality Edges ===
      {'type': 'functionality', 'source': 'material_assessment', 'target': 'design_prediction', 'label': 'stiffness_to_weight', 'weight': 1.0},
      {'type': 'functionality', 'source': 'material_assessment', 'target': 'design_prediction', 'label': 'buckling_resistance', 'weight': 0.8},
      {'type': 'functionality', 'source': 'material_prediction', 'target': 'design_prediction', 'label': 'durability', 'weight': 0.7}
    ]
  }
]
