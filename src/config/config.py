# This file contains the scenario configurations as a Python list.

SCENARIOS = [
  {
    'name': "Lightweight Aluminum Frame",
    'nodes': [
      {'node_id': 'material_assessment', 'domain': 'Material', 'node_type': 'Assessment', 'attributes': {'embodied_carbon': 6.8, 'cost_per_kg': 3.5, 'stiffness': 70}, 'function_path': 'models.system.material_metrics'},
      {'node_id': 'design_creation', 'domain': 'Design', 'node_type': 'Creation'},
      {'node_id': 'design_prediction', 'domain': 'Design', 'node_type': 'Prediction', 'attributes': {'stress_fail_rate': 0.05}, 'function_path': 'models.system.design_performance'},
      {'node_id': 'technology_assessment', 'domain': 'Manufacturing', 'node_type': 'Assessment', 'attributes': {'energy_consumption': 15, 'waste_rate': 0.1}, 'function_path': 'models.system.manufacturing_metrics'}
    ],
    'edges': [
      {'type': 'value', 'source': 'material_assessment', 'target': 'technology_assessment', 'label': 'cost', 'weight': 0.7},
      {'type': 'value', 'source': 'material_assessment', 'target': 'design_prediction', 'label': 'sustainability', 'weight': 0.8},
      {'type': 'functionality', 'source': 'material_assessment', 'target': 'design_prediction', 'label': 'structural_rigidity', 'weight': 0.9},
      {'type': 'dependency', 'sources': ['material_assessment', 'design_creation'], 'target': 'design_prediction'}
    ]
  },
    {
    'name': "High-Strength Steel Frame",
    'nodes': [
      {'node_id': 'material_assessment', 'domain': 'Material', 'node_type': 'Assessment', 'attributes': {'embodied_carbon': 12.1, 'cost_per_kg': 1.2, 'stiffness': 200}, 'function_path': 'models.system.material_metrics'},
      {'node_id': 'design_creation', 'domain': 'Design', 'node_type': 'Creation'},
      {'node_id': 'design_prediction', 'domain': 'Design', 'node_type': 'Prediction', 'attributes': {'stress_fail_rate': 0.02}, 'function_path': 'models.system.design_performance'},
      {'node_id': 'technology_assessment', 'domain': 'Manufacturing', 'node_type': 'Assessment', 'attributes': {'energy_consumption': 25, 'waste_rate': 0.05}, 'function_path': 'models.system.manufacturing_metrics'}
    ],
    'edges': [
      {'type': 'value', 'source': 'material_assessment', 'target': 'technology_assessment', 'label': 'cost', 'weight': 0.9},
      {'type': 'value', 'source': 'material_assessment', 'target': 'technology_assessment', 'label': 'sustainability', 'weight': 0.5},
      {'type': 'functionality', 'source': 'material_assessment', 'target': 'design_prediction', 'label': 'structural_rigidity', 'weight': 0.95},
      {'type': 'dependency', 'sources': ['material_assessment', 'design_creation'], 'target': 'design_prediction'}
    ]
  }
]