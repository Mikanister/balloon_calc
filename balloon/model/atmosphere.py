"""
Модель атмосфери: тиск, щільність, температура на різних висотах
"""

from typing import Tuple

from balloon.constants import (
    T0, LAPSE_RATE, SEA_LEVEL_PRESSURE, 
    SEA_LEVEL_AIR_DENSITY, GAS_CONSTANT, GRAVITY
)


def air_density_at_height(h: float, ground_temp_C: float) -> Tuple[float, float, float]:
    """
    Розраховує температуру, щільність та тиск повітря на висоті
    
    Використовує стандартну атмосферну модель з лінійним градієнтом температури.
    
    Args:
        h: Висота над рівнем моря (м)
        ground_temp_C: Температура на землі (°C)
    
    Returns:
        Tuple[температура_°C, щільність_кг/м³, тиск_Па]
    
    Example:
        >>> temp, rho, pressure = air_density_at_height(1000, 15)
        >>> temp < 15  # Температура знижується з висотою
        True
        >>> pressure < SEA_LEVEL_PRESSURE  # Тиск знижується
        True
    """
    T_sea = ground_temp_C + T0
    T = T_sea - LAPSE_RATE * h
    P = SEA_LEVEL_PRESSURE * (T / T_sea) ** (GRAVITY / (GAS_CONSTANT * LAPSE_RATE))
    rho = P / (GAS_CONSTANT * T)
    return T - T0, rho, P

