"""
Module d’algorithme de triangulation.

Cette implémentation utilise une version simplifiée de l’algorithme
Ear-Clipping, suffisant pour le cadre du TP.
"""

from __future__ import annotations
from typing import List, Tuple
from .triangles import triangle_area, are_points_collinear


def simple_triangulation(
    points: List[Tuple[float, float]]
) -> List[Tuple[int, int, int]]:
    """
    Calcule une triangulation simple d’un ensemble de points.

    Args:
        points: Liste de points (x, y)

    Returns:
        Liste de triangles sous forme de triplets d’indices.

    Raises:
        ValueError: Si moins de 3 points ou si tous les points sont alignés.
    """

    # Minimum requis
    if len(points) < 3:
        raise ValueError("Impossible de trianguler : moins de 3 points.")

    # Vérifier si colinéaires
    collinear_count = 0
    for i in range(len(points) - 2):
        if are_points_collinear(points[i], points[i + 1], points[i + 2]):
            collinear_count += 1
    if collinear_count == len(points) - 2:
        return []

    # Indices de travail
    remaining = list(range(len(points)))
    triangles = []

    def is_convex(a, b, c):
        """Détermine la convexité du coin."""
        return triangle_area(points[a], points[b], points[c]) > 0

    def contains_no_other_point(a, b, c):
        """Vérifie qu'aucun point n'est dans le triangle."""
        ax, ay = points[a]
        bx, by = points[b]
        cx, cy = points[c]

        def area(px, py, qx, qy, rx, ry):
            return (qx - px) * (ry - py) - (qy - py) * (rx - px)

        for p in remaining:
            if p in (a, b, c):
                continue
            px, py = points[p]
            # barycentriques signés
            if (
                area(ax, ay, bx, by, px, py) > 0
                and area(bx, by, cx, cy, px, py) > 0
                and area(cx, cy, ax, ay, px, py) > 0
            ):
                return False
        return True

    # Ear clipping
    while len(remaining) > 3:
        ear_found = False

        for i in range(len(remaining)):
            a = remaining[i - 1]
            b = remaining[i]
            c = remaining[(i + 1) % len(remaining)]

            if is_convex(a, b, c) and contains_no_other_point(a, b, c):
                triangles.append((a, b, c))
                del remaining[i]
                ear_found = True
                break

        if not ear_found:
            raise ValueError(
    "Triangulation impossible : polygone non simple "
    "ou problème géométrique."
)


    triangles.append(tuple(remaining))
    return triangles


def bounding_triangle(
        points: List[Tuple[float, float]]
        ) -> Tuple[Tuple[float, float], ...]:
    """
    Crée un triangle englobant (optionnel pour le TP).

    Args:
        points: Liste des points

    Returns:
        Un triangle très large englobant tous les points.
    """
    if not points:
        raise ValueError("Aucun point pour créer un triangle englobant.")

    min_x = min(p[0] for p in points)
    max_x = max(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)

    dx = max_x - min_x
    dy = max_y - min_y
    d = max(dx, dy) * 10  # marge large

    return (
        (min_x - d, min_y - d),
        (max_x + d, min_y - d),
        (min_x, max_y + d),
    )


def is_point_in_triangle(
    p: Tuple[float, float],
    a: Tuple[float, float],
    b: Tuple[float, float],
    c: Tuple[float, float],
) -> bool:
    """
    Teste si un point est dans un triangle en utilisant les coordonnées barycentriques.
    """

    def det(u, v, w):
        return (v[0] - u[0]) * (w[1] - u[1]) - (v[1] - u[1]) * (w[0] - u[0])

    d1 = det(p, a, b)
    d2 = det(p, b, c)
    d3 = det(p, c, a)

    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

    # Le point est dans le triangle si les signes sont tous identiques
    return not (has_neg and has_pos)
