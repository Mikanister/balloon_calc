"""
Модель газів: гелій, водень, гаряче повітря
"""

from balloon.constants import (
    GAS_SPECIFIC_CONSTANT, GAS_CONSTANT, T0, SEA_LEVEL_AIR_DENSITY
)


def calculate_gas_density_at_altitude(
    gas_type: str, 
    pressure: float, 
    temperature_K: float
) -> float:
    """
    Розраховує щільність газу на висоті за ідеальним газовим законом
    
    Використовує рівняння стану ідеального газу: ρ = P/(R_specific * T)
    
    Args:
        gas_type: Тип газу ("Гелій", "Водень", "Гаряче повітря")
        pressure: Тиск на висоті (Па)
        temperature_K: Температура на висоті (К)
    
    Returns:
        Щільність газу на висоті (кг/м³)
    
    Raises:
        ValueError: Якщо тип газу не підтримується
    
    Example:
        >>> # Гелій на рівні моря при 15°C
        >>> rho = calculate_gas_density_at_altitude("Гелій", 101325, 288.15)
        >>> rho > 0
        True
    """
    if gas_type == "Гаряче повітря":
        # Для гарячого повітря використовується GAS_CONSTANT
        return pressure / (GAS_CONSTANT * temperature_K)
    else:
        # Для гелію та водню використовуємо питому газову сталу
        R_specific = GAS_SPECIFIC_CONSTANT.get(gas_type)
        if R_specific is None:
            raise ValueError(f"Непідтримуваний тип газу: {gas_type}")
        return pressure / (R_specific * temperature_K)


def calculate_hot_air_density(inside_temp_C: float) -> float:
    """
    Розраховує щільність гарячого повітря
    
    Використовує спрощену модель: щільність обернено пропорційна температурі
    (припускаємо постійний тиск).
    
    Args:
        inside_temp_C: Температура всередині кулі (°C)
    
    Returns:
        Щільність гарячого повітря (кг/м³)
    
    Example:
        >>> # Гаряче повітря при 100°C має меншу щільність ніж при 15°C
        >>> rho_100 = calculate_hot_air_density(100)
        >>> rho_15 = calculate_hot_air_density(15)
        >>> rho_100 < rho_15
        True
    """
    T_inside = inside_temp_C + T0
    return SEA_LEVEL_AIR_DENSITY * T0 / T_inside

