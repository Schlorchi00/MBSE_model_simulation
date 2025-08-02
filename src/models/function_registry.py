from .system_functions import (
    material_search,
    material_assessment,
    material_prediction,
    design_creation,
    design_assembly,
    design_prediction,
    technology_selection,
    manufacturing_assessment,
    technology_simulation
)

MODEL_FUNCTIONS = {
    'models.system.material_search': material_search,
    'models.system.material_assessment': material_assessment,
    'models.system.material_prediction': material_prediction,
    'models.system.design_creation': design_creation,
    'models.system.design_assembly': design_assembly,
    'models.system.design_prediction': design_prediction,
    'models.system.technology_selection': technology_selection,
    'models.system.manufacturing_assessment': manufacturing_assessment,
    'models.system.technology_simulation': technology_simulation,
}
