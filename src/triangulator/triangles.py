"""
Fonctions utilitaires liées aux triangles.
Ce module fournit les briques mathématiques nécessaires à la triangulation.
"""

from __future__ import annotations
from typing import List, Tuple


def validate_triangle_indices(
    points: List[Tuple[float, float]],
    a: int,
    b: int,
    c: int,
) -> bool:
    """
    Vérifie que les indices a, b et c représentent bien un triangle valide.

    Conditions :
    - Les indices doivent être dans les bornes de la liste des points.
    - Les trois indices doivent être distincts.

    Retourne True si le triangle est valide, False sinon.
    """
    n = len(points)

    if a < 0 or b < 0 or c < 0:
        return False
    if a >= n or b >= n or c >= n:
        return False
    if len({a, b, c}) != 3:
        return False

    return True


def triangle_area(p1: Tuple[float, float],
                  p2: Tuple[float, float],
                  p3: Tuple[float, float]) -> float:
    """
    Calcule l’aire d’un triangle défini par 3 points.

    Aire = |(x1(y2 - y3) + x2(y3 - y1) + x3(y1 - y2)) / 2|

    Retourne une valeur positive, ou 0 si les points sont alignés.
    """
    (x1, y1), (x2, y2), (x3, y3) = p1, p2, p3

    return abs(
        x1 * (y2 - y3)
        + x2 * (y3 - y1)
        + x3 * (y1 - y2)
    ) / 2.0


def are_points_collinear(p1: Tuple[float, float],
                         p2: Tuple[float, float],
                         p3: Tuple[float, float],
                         epsilon: float = 1e-10) -> bool:
    """
    Retourne True si les trois points sont alignés.

    On considère que l’aire ≈ 0 implique colinéarité.
    """
    return triangle_area(p1, p2, p3) < epsilon


def validate_triangulation(points: List[Tuple[float, float]],
                           triangles: List[Tuple[int, int, int]]) -> bool:
    """
    Vérifie qu’une triangulation est correcte.

    Conditions :
    - Chaque triangle doit avoir des indices valides.
    - Aucun triangle ne doit être dégénéré (aire = 0).
    """
    for a, b, c in triangles:
        if not validate_triangle_indices(points, a, b, c):
            return False

        p1, p2, p3 = points[a], points[b], points[c]
        if are_points_collinear(p1, p2, p3):
            return False

    return True
