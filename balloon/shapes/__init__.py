"""
Модуль для розрахунків форм аеростатів
"""

# Експортуємо функції з окремих модулів
try:
    from balloon.shapes.sphere import (
        sphere_volume,
        sphere_surface_area,
        sphere_radius_from_volume
    )
    from balloon.shapes.pillow import (
        pillow_volume,
        pillow_surface_area,
        pillow_dimensions_from_volume
    )
    from balloon.shapes.pear import (
        pear_volume,
        pear_surface_area,
        pear_dimensions_from_volume
    )
    from balloon.shapes.cigar import (
        cigar_volume,
        cigar_surface_area,
        cigar_dimensions_from_volume
    )
    # Примітка: cylinder та torus залишені в окремих модулях для тестів,
    # але не експортуються, оскільки не підтримуються в основному коді
except ImportError:
    # Fallback для сумісності (використовується тільки в exe)
    from shapes.sphere import (
        sphere_volume,
        sphere_surface_area,
        sphere_radius_from_volume
    )
    from shapes.pillow import (
        pillow_volume,
        pillow_surface_area,
        pillow_dimensions_from_volume
    )
    from shapes.pear import (
        pear_volume,
        pear_surface_area,
        pear_dimensions_from_volume
    )
    from shapes.cigar import (
        cigar_volume,
        cigar_surface_area,
        cigar_dimensions_from_volume
    )

__all__ = [
    # Sphere
    'sphere_volume',
    'sphere_surface_area',
    'sphere_radius_from_volume',
    # Pillow
    'pillow_volume',
    'pillow_surface_area',
    'pillow_dimensions_from_volume',
    # Pear
    'pear_volume',
    'pear_surface_area',
    'pear_dimensions_from_volume',
    # Cigar
    'cigar_volume',
    'cigar_surface_area',
    'cigar_dimensions_from_volume',
    # Примітка: cylinder та torus не експортуються - вони доступні
    # тільки через прямі імпорти для тестів, але не підтримуються
    # в основному коді (SHAPES реєстрі, GUI, валідації)
]

