from .system_functions import (
    calculate_material_metrics,
    calculate_design_performance,
    calculate_manufacturing_metrics
)

MODEL_FUNCTIONS = {
    'models.system.material_metrics': calculate_material_metrics,
    'models.system.design_performance': calculate_design_performance,
    'models.system.manufacturing_metrics': calculate_manufacturing_metrics,
}