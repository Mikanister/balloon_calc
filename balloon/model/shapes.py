"""
Модель форм: об'єм, площа поверхні, розміри
"""

from typing import Dict, Any, Optional, Literal, Tuple
import math

from balloon.shapes import (
    sphere_volume,
    sphere_surface_area,
    sphere_radius_from_volume,
    pillow_volume,
    pillow_surface_area,
    pillow_dimensions_from_volume,
    pear_volume,
    pear_surface_area,
    pear_dimensions_from_volume,
    cigar_volume,
    cigar_surface_area,
    cigar_dimensions_from_volume,
)


class ShapeGeometry:
    """
    Геометрія форми оболонки
    
    Attributes:
        shape_type: Тип форми ("sphere", "pillow", "pear", "cigar")
        volume: Об'єм (м³)
        surface_area: Площа поверхні (м²)
        characteristic_radius: Характерний радіус (м)
        dimensions: Словник з розмірами форми
    """
    
    def __init__(
        self,
        shape_type: Literal["sphere", "pillow", "pear", "cigar"],
        volume: float,
        surface_area: float,
        characteristic_radius: float,
        dimensions: Dict[str, float]
    ):
        self.shape_type = shape_type
        self.volume = volume
        self.surface_area = surface_area
        self.characteristic_radius = characteristic_radius
        self.dimensions = dimensions


def get_shape_volume(
    shape_type: Literal["sphere", "pillow", "pear", "cigar"],
    dimensions: Dict[str, float]
) -> float:
    """
    Розраховує об'єм форми
    
    Args:
        shape_type: Тип форми
        dimensions: Словник з розмірами форми
    
    Returns:
        Об'єм (м³)
    """
    if shape_type == "sphere":
        radius = dimensions.get("radius", 0)
        return sphere_volume(radius)
    elif shape_type == "pillow":
        length = dimensions.get("pillow_len", 0)
        width = dimensions.get("pillow_wid", 0)
        thickness = dimensions.get("pillow_height", 1.0)
        return pillow_volume(length, width, thickness)
    elif shape_type == "pear":
        height = dimensions.get("pear_height", 0)
        top_radius = dimensions.get("pear_top_radius", 0)
        bottom_radius = dimensions.get("pear_bottom_radius", 0)
        return pear_volume(height, top_radius, bottom_radius)
    elif shape_type == "cigar":
        length = dimensions.get("cigar_length", 0)
        radius = dimensions.get("cigar_radius", 0)
        return cigar_volume(length, radius)
    else:
        raise ValueError(f"Непідтримуваний тип форми: {shape_type}")


def get_shape_surface_area(
    shape_type: Literal["sphere", "pillow", "pear", "cigar"],
    dimensions: Dict[str, float]
) -> float:
    """
    Розраховує площу поверхні форми
    
    Args:
        shape_type: Тип форми
        dimensions: Словник з розмірами форми
    
    Returns:
        Площа поверхні (м²)
    """
    if shape_type == "sphere":
        radius = dimensions.get("radius", 0)
        return sphere_surface_area(radius)
    elif shape_type == "pillow":
        length = dimensions.get("pillow_len", 0)
        width = dimensions.get("pillow_wid", 0)
        return pillow_surface_area(length, width)
    elif shape_type == "pear":
        height = dimensions.get("pear_height", 0)
        top_radius = dimensions.get("pear_top_radius", 0)
        bottom_radius = dimensions.get("pear_bottom_radius", 0)
        return pear_surface_area(height, top_radius, bottom_radius)
    elif shape_type == "cigar":
        length = dimensions.get("cigar_length", 0)
        radius = dimensions.get("cigar_radius", 0)
        return cigar_surface_area(length, radius)
    else:
        raise ValueError(f"Непідтримуваний тип форми: {shape_type}")


def get_shape_dimensions_from_volume(
    shape_type: Literal["sphere", "pillow", "pear", "cigar"],
    target_volume: float,
    partial_params: Optional[Dict[str, float]] = None
) -> Tuple[float, float, float, Dict[str, float]]:
    """
    Розраховує розміри форми на основі об'єму
    
    Args:
        shape_type: Тип форми
        target_volume: Цільовий об'єм (м³)
        partial_params: Часткові параметри (якщо задані, використовуються)
    
    Returns:
        Tuple[об'єм, площа_поверхні, характерний_радіус, словник_розмірів]
    """
    partial_params = partial_params or {}
    
    if shape_type == "sphere":
        r = sphere_radius_from_volume(target_volume)
        surface = sphere_surface_area(r)
        return target_volume, surface, r, {"radius": r}
    
    elif shape_type == "pillow":
        L = partial_params.get("pillow_len")
        W = partial_params.get("pillow_wid")
        L, W, H = pillow_dimensions_from_volume(
            target_volume,
            length=float(L) if L else None,
            width=float(W) if W else None
        )
        surface = pillow_surface_area(L, W)
        char_r = min(L, W) / 2
        return target_volume, surface, char_r, {"pillow_len": L, "pillow_wid": W}
    
    elif shape_type == "pear":
        H = partial_params.get("pear_height")
        R_top = partial_params.get("pear_top_radius")
        R_bottom = partial_params.get("pear_bottom_radius")
        H, R_top, R_bottom = pear_dimensions_from_volume(
            target_volume,
            height=float(H) if H else None,
            top_radius=float(R_top) if R_top else None,
            bottom_radius=float(R_bottom) if R_bottom else None
        )
        surface = pear_surface_area(H, R_top, R_bottom)
        char_r = (R_top + R_bottom) / 2
        return target_volume, surface, char_r, {
            "pear_height": H,
            "pear_top_radius": R_top,
            "pear_bottom_radius": R_bottom
        }
    
    elif shape_type == "cigar":
        L = partial_params.get("cigar_length")
        R = partial_params.get("cigar_radius")
        L, R = cigar_dimensions_from_volume(
            target_volume,
            length=float(L) if L else None,
            radius=float(R) if R else None
        )
        surface = cigar_surface_area(L, R)
        char_r = R
        return target_volume, surface, char_r, {"cigar_length": L, "cigar_radius": R}
    
    else:
        raise ValueError(f"Непідтримуваний тип форми: {shape_type}")

