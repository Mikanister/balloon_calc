"""
Додаткові функції аналізу та візуалізації для аеростатів
"""

import math
from typing import List, Tuple, Dict, Any
from constants import *
from calculations import air_density_at_height, calculate_hot_air_density


def calculate_optimal_height(gas_type: str, material: str, thickness_mm: float, 
                           gas_volume: float, ground_temp: float = 15, 
                           inside_temp: float = 100) -> Dict[str, Any]:
    """
    Розраховує оптимальну висоту польоту для максимального навантаження
    
    Args:
        gas_type: Тип газу
        material: Матеріал оболонки
        thickness_mm: Товщина оболонки (мкм)
        gas_volume: Об'єм газу (м³)
        ground_temp: Температура на землі (°C)
        inside_temp: Температура всередині (°C)
    
    Returns:
        Словник з оптимальними параметрами
    """
    thickness = thickness_mm / 1e6
    max_payload = 0
    optimal_height = 0
    optimal_params = {}
    
    # Перевіряємо висоти від 0 до 50 км
    for height in range(0, 50001, 100):
        try:
            T_outside_C, rho_air, P_outside = air_density_at_height(height, ground_temp)
            
            # Розрахунок щільності газу
            if gas_type == "Гаряче повітря":
                rho_gas = calculate_hot_air_density(inside_temp)
            else:
                rho_gas = GAS_DENSITY[gas_type]
            
            net_lift_per_m3 = rho_air - rho_gas
            
            if net_lift_per_m3 > 0:
                # Розрахунок об'єму на висоті
                T_outside = T_outside_C + T0
                required_volume = gas_volume * SEA_LEVEL_PRESSURE / P_outside * T_outside / (ground_temp + T0)
                
                # Розрахунок маси оболонки
                surface_area = (required_volume * 6 / math.pi) ** (2 / 3)
                mass_shell = surface_area * thickness * MATERIALS[material][0]
                
                # Розрахунок навантаження
                lift = net_lift_per_m3 * gas_volume
                payload = lift - mass_shell
                
                if payload > max_payload:
                    max_payload = payload
                    optimal_height = height
                    optimal_params = {
                        'height': height,
                        'payload': payload,
                        'lift': lift,
                        'mass_shell': mass_shell,
                        'rho_air': rho_air,
                        'net_lift_per_m3': net_lift_per_m3,
                        'T_outside_C': T_outside_C,
                        'P_outside': P_outside
                    }
                    
        except Exception:
            continue
    
    return optimal_params


def calculate_height_profile(gas_type: str, material: str, thickness_mm: float,
                           gas_volume: float, ground_temp: float = 15,
                           inside_temp: float = 100, max_height: int = 50000) -> List[Dict[str, Any]]:
    """
    Розраховує профіль параметрів по висоті
    
    Args:
        gas_type: Тип газу
        material: Матеріал оболонки
        thickness_mm: Товщина оболонки (мкм)
        gas_volume: Об'єм газу (м³)
        ground_temp: Температура на землі (°C)
        inside_temp: Температура всередині (°C)
        max_height: Максимальна висота для аналізу (м)
    
    Returns:
        Список словників з параметрами на різних висотах
    """
    thickness = thickness_mm / 1e6
    profile = []
    
    for height in range(0, max_height + 1, 500):
        try:
            T_outside_C, rho_air, P_outside = air_density_at_height(height, ground_temp)
            
            # Розрахунок щільності газу
            if gas_type == "Гаряче повітря":
                rho_gas = calculate_hot_air_density(inside_temp)
            else:
                rho_gas = GAS_DENSITY[gas_type]
            
            net_lift_per_m3 = rho_air - rho_gas
            
            if net_lift_per_m3 > 0:
                # Розрахунок об'єму на висоті
                T_outside = T_outside_C + T0
                required_volume = gas_volume * SEA_LEVEL_PRESSURE / P_outside * T_outside / (ground_temp + T0)
                
                # Розрахунок маси оболонки
                surface_area = (required_volume * 6 / math.pi) ** (2 / 3)
                mass_shell = surface_area * thickness * MATERIALS[material][0]
                
                # Розрахунок навантаження
                lift = net_lift_per_m3 * gas_volume
                payload = lift - mass_shell
                
                profile.append({
                    'height': height,
                    'payload': payload,
                    'lift': lift,
                    'mass_shell': mass_shell,
                    'rho_air': rho_air,
                    'net_lift_per_m3': net_lift_per_m3,
                    'T_outside_C': T_outside_C,
                    'P_outside': P_outside,
                    'required_volume': required_volume
                })
            else:
                # Газ не має підйомної сили на цій висоті
                profile.append({
                    'height': height,
                    'payload': 0,
                    'lift': 0,
                    'mass_shell': 0,
                    'rho_air': rho_air,
                    'net_lift_per_m3': net_lift_per_m3,
                    'T_outside_C': T_outside_C,
                    'P_outside': P_outside,
                    'required_volume': 0
                })
                
        except Exception:
            continue
    
    return profile


def calculate_material_comparison(gas_type: str, thickness_mm: float, gas_volume: float,
                                ground_temp: float = 15, inside_temp: float = 100,
                                height: float = 1000) -> Dict[str, Dict[str, float]]:
    """
    Порівнює різні матеріали оболонки
    
    Args:
        gas_type: Тип газу
        thickness_mm: Товщина оболонки (мкм)
        gas_volume: Об'єм газу (м³)
        ground_temp: Температура на землі (°C)
        inside_temp: Температура всередині (°C)
        height: Висота польоту (м)
    
    Returns:
        Словник з результатами для кожного матеріалу
    """
    results = {}
    
    for material in MATERIALS.keys():
        try:
            thickness = thickness_mm / 1e6
            T_outside_C, rho_air, P_outside = air_density_at_height(height, ground_temp)
            
            # Розрахунок щільності газу
            if gas_type == "Гаряче повітря":
                rho_gas = calculate_hot_air_density(inside_temp)
            else:
                rho_gas = GAS_DENSITY[gas_type]
            
            net_lift_per_m3 = rho_air - rho_gas
            
            if net_lift_per_m3 > 0:
                # Розрахунок об'єму на висоті
                T_outside = T_outside_C + T0
                required_volume = gas_volume * SEA_LEVEL_PRESSURE / P_outside * T_outside / (ground_temp + T0)
                
                # Розрахунок маси оболонки
                surface_area = (required_volume * 6 / math.pi) ** (2 / 3)
                mass_shell = surface_area * thickness * MATERIALS[material][0]
                
                # Розрахунок навантаження
                lift = net_lift_per_m3 * gas_volume
                payload = lift - mass_shell
                
                # Розрахунок напруги
                radius = ((3 * required_volume) / (4 * math.pi)) ** (1 / 3)
                stress = 0  # Для газів без внутрішнього тиску
                if gas_type == "Гаряче повітря":
                    P_inside = rho_gas * GAS_CONSTANT * (inside_temp + T0)
                    stress = max(0, P_inside - P_outside) * radius / (2 * thickness)
                
                stress_limit = MATERIALS[material][1]
                safety_factor = stress_limit / stress if stress > 0 else float('inf')
                
                results[material] = {
                    'payload': payload,
                    'mass_shell': mass_shell,
                    'lift': lift,
                    'stress': stress,
                    'stress_limit': stress_limit,
                    'safety_factor': safety_factor,
                    'density': MATERIALS[material][0]
                }
                
        except Exception:
            results[material] = {
                'payload': 0,
                'mass_shell': 0,
                'lift': 0,
                'stress': 0,
                'stress_limit': MATERIALS[material][1],
                'safety_factor': 0,
                'density': MATERIALS[material][0]
            }
    
    return results


def calculate_cost_analysis(material: str, thickness_mm: float, gas_volume: float,
                          gas_type: str, ground_temp: float = 15, 
                          inside_temp: float = 100, height: float = 1000) -> Dict[str, float]:
    """
    Розраховує приблизну вартість матеріалів
    
    Args:
        material: Матеріал оболонки
        thickness_mm: Товщина оболонки (мкм)
        gas_volume: Об'єм газу (м³)
        gas_type: Тип газу
        ground_temp: Температура на землі (°C)
        inside_temp: Температура всередині (°C)
        height: Висота польоту (м)
    
    Returns:
        Словник з вартісними показниками
    """
    # Приблизні ціни на матеріали (грн/кг)
    material_prices = {
        "HDPE": 25,
        "TPU": 80,
        "Mylar": 120,
        "Nylon": 60,
        "PET": 35
    }
    
    # Ціни на гази (грн/м³)
    gas_prices = {
        "Гелій": 150,
        "Водень": 5,
        "Гаряче повітря": 0.1  # вартість нагріву
    }
    
    try:
        thickness = thickness_mm / 1e6
        T_outside_C, rho_air, P_outside = air_density_at_height(height, ground_temp)
        
        # Розрахунок щільності газу
        if gas_type == "Гаряче повітря":
            rho_gas = calculate_hot_air_density(inside_temp)
        else:
            rho_gas = GAS_DENSITY[gas_type]
        
        net_lift_per_m3 = rho_air - rho_gas
        
        if net_lift_per_m3 > 0:
            # Розрахунок об'єму на висоті
            T_outside = T_outside_C + T0
            required_volume = gas_volume * SEA_LEVEL_PRESSURE / P_outside * T_outside / (ground_temp + T0)
            
            # Розрахунок маси оболонки
            surface_area = (required_volume * 6 / math.pi) ** (2 / 3)
            mass_shell = surface_area * thickness * MATERIALS[material][0]
            
            # Розрахунок вартості
            material_cost = mass_shell * material_prices.get(material, 50)
            gas_cost = gas_volume * gas_prices.get(gas_type, 0)
            total_cost = material_cost + gas_cost
            
            return {
                'material_cost': material_cost,
                'gas_cost': gas_cost,
                'total_cost': total_cost,
                'mass_shell': mass_shell,
                'gas_volume': gas_volume,
                'cost_per_kg_payload': total_cost / max(0.001, net_lift_per_m3 * gas_volume - mass_shell)
            }
            
    except Exception:
        pass
    
    return {
        'material_cost': 0,
        'gas_cost': 0,
        'total_cost': 0,
        'mass_shell': 0,
        'gas_volume': gas_volume,
        'cost_per_kg_payload': 0
    }


def generate_report(results: Dict[str, Any], mode: str, inputs: Dict[str, Any]) -> str:
    """
    Генерує текстовий звіт з результатами
    
    Args:
        results: Результати розрахунків
        mode: Режим розрахунку
        inputs: Вхідні параметри
    
    Returns:
        Текстовий звіт
    """
    report = []
    report.append("=" * 60)
    report.append("ЗВІТ ПО РОЗРАХУНКУ АЕРОСТАТА")
    report.append("=" * 60)
    report.append("")
    
    # Вхідні параметри
    report.append("ВХІДНІ ПАРАМЕТРИ:")
    report.append("-" * 30)
    report.append(f"Режим розрахунку: {'Обʼєм ➜ навантаження' if mode == 'payload' else 'Навантаження ➜ обʼєм'}")
    report.append(f"Тип газу: {inputs['gas_type']}")
    report.append(f"Матеріал оболонки: {inputs['material']}")
    report.append(f"Товщина оболонки: {inputs['thickness']} мкм")
    report.append(f"Висота пуску: {inputs['start_height']} м")
    report.append(f"Висота польоту: {inputs['work_height']} м")
    
    if inputs['gas_type'] == "Гаряче повітря":
        report.append(f"Температура на землі: {inputs['ground_temp']} °C")
        report.append(f"Температура всередині: {inputs['inside_temp']} °C")
    
    report.append("")
    
    # Результати
    report.append("РЕЗУЛЬТАТИ РОЗРАХУНКІВ:")
    report.append("-" * 30)
    
    if mode == "volume":
        report.append(f"Потрібний обʼєм газу: {results['gas_volume']:.2f} м³")
    
    report.extend([
        f"Необхідний обʼєм кулі: {results['required_volume']:.2f} м³",
        f"Корисне навантаження: {results['payload']:.2f} кг",
        f"Маса оболонки: {results['mass_shell']:.2f} кг",
        f"Підйомна сила: {results['lift']:.2f} кг",
        f"Радіус кулі: {results['radius']:.2f} м",
        f"Площа поверхні: {results['surface_area']:.2f} м²",
        f"Щільність повітря: {results['rho_air']:.4f} кг/м³",
        f"Підйомна сила на м³: {results['net_lift_per_m3']:.4f} кг/м³"
    ])
    
    if inputs['gas_type'] == "Гаряче повітря":
        if results['stress'] > 0:
            safety_factor = results['stress_limit'] / results['stress']
        else:
            safety_factor = float('inf')
        report.extend([
            f"Температура зовні: {results['T_outside_C']:.1f} °C",
            f"Максимальна напруга: {results['stress'] / 1e6:.2f} МПа",
            f"Допустима напруга: {results['stress_limit'] / 1e6:.1f} МПа",
            f"Коефіцієнт безпеки: {'∞' if safety_factor == float('inf') else f'{safety_factor:.1f}'}"
        ])
        if safety_factor < 2:
            report.append("⚠️  УВАГА: Низький коефіцієнт безпеки!")
    
    report.append("")
    report.append("=" * 60)
    
    return '\n'.join(report) 