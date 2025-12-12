"""
Модуль для аналізу аеростатів
"""

# Експортуємо функції з окремих модулів
try:
    from balloon.analysis.optimal_height import calculate_optimal_height
    from balloon.analysis.height_profile import calculate_height_profile
    from balloon.analysis.material_comparison import calculate_material_comparison
    from balloon.analysis.cost_analysis import calculate_cost_analysis
    from balloon.analysis.flight_time import calculate_max_flight_time
    from balloon.analysis.report import generate_report
    from balloon.analysis.base import _compute_lift_state
except ImportError:
    from analysis.optimal_height import calculate_optimal_height
    from analysis.height_profile import calculate_height_profile
    from analysis.material_comparison import calculate_material_comparison
    from analysis.cost_analysis import calculate_cost_analysis
    from analysis.flight_time import calculate_max_flight_time
    from analysis.report import generate_report
    from analysis.base import _compute_lift_state

__all__ = [
    'calculate_optimal_height',
    'calculate_height_profile',
    'calculate_material_comparison',
    'calculate_cost_analysis',
    'calculate_max_flight_time',
    'generate_report',
    '_compute_lift_state',
]

