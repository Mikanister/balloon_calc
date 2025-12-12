"""
Модель матеріалів: щільність, міцність, проникність
"""

from typing import Optional

try:
    from baloon.constants import MATERIALS, PERMEABILITY
except ImportError:
    from constants import MATERIALS, PERMEABILITY


def get_material_density(material: str) -> float:
    """
    Повертає щільність матеріалу
    
    Args:
        material: Назва матеріалу
    
    Returns:
        Щільність (кг/м³)
    
    Raises:
        KeyError: Якщо матеріал не знайдено
    """
    if material not in MATERIALS:
        raise KeyError(f"Матеріал '{material}' не знайдено. Доступні: {list(MATERIALS.keys())}")
    return MATERIALS[material][0]


def get_material_stress_limit(material: str) -> float:
    """
    Повертає допустиму напругу матеріалу
    
    Args:
        material: Назва матеріалу
    
    Returns:
        Допустима напруга (Па)
    
    Raises:
        KeyError: Якщо матеріал не знайдено
    """
    if material not in MATERIALS:
        raise KeyError(f"Матеріал '{material}' не знайдено. Доступні: {list(MATERIALS.keys())}")
    return MATERIALS[material][1]


def get_material_permeability(material: str, gas_type: str) -> Optional[float]:
    """
    Повертає коефіцієнт проникності матеріалу для газу
    
    Args:
        material: Назва матеріалу
        gas_type: Тип газу ("Гелій" або "Водень")
    
    Returns:
        Коефіцієнт проникності (м²/(с·Па)) або None, якщо не знайдено
    """
    if material not in PERMEABILITY:
        return None
    return PERMEABILITY[material].get(gas_type)


def calc_stress(p_internal: float, p_external: float, r: float, t: float) -> float:
    """
    Розраховує напругу в оболонці кулі
    
    Використовує формулу для тонкостінної сферичної оболонки:
    σ = ΔP * r / (2 * t)
    
    Args:
        p_internal: Внутрішній тиск (Па)
        p_external: Зовнішній тиск (Па)
        r: Характерний радіус кулі (м)
        t: Товщина оболонки (м)
    
    Returns:
        Напруга (Па)
    
    Example:
        >>> # Напруга в оболонці з радіусом 1м, товщиною 0.0001м, різницею тисків 1000Па
        >>> stress = calc_stress(101325, 100325, 1.0, 0.0001)
        >>> stress > 0
        True
    """
    if t == 0:
        return 0.0
    delta_p = max(0, p_internal - p_external)
    return delta_p * r / (2 * t)

