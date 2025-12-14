import time
import random
import pytest

from triangulator.triangulation import simple_triangulation
from triangulator.serialisation import (
    pointset_to_binary,
    binary_to_pointset,
    triangles_to_binary,
    binary_to_triangles,
)


# ------------------------------------------------------------
# OUTILS : génération d’un polygone convexe pour triangulation
# ------------------------------------------------------------

def generer_polygone_convexe(n):
    """
    Génère n points formant un polygone convexe.
    Les points sont triés par angle autour du centre.
    """
    points = [(random.random(), random.random()) for _ in range(n)]
    cx = sum(p[0] for p in points) / n
    cy = sum(p[1] for p in points) / n

    points = sorted(points, key=lambda p: (p[0] - cx, p[1] - cy))
    return points


# ------------------------------------------------------------
# TESTS PERFORMANCE TRIANGULATION
# ------------------------------------------------------------

@pytest.mark.perf
def test_triangulation_10_points():
    points = generer_polygone_convexe(10)
    debut = time.perf_counter()

    tris = simple_triangulation(points)

    duree = time.perf_counter() - debut
    assert duree < 0.05  # 50 ms
    assert len(tris) > 0


@pytest.mark.perf
def test_triangulation_100_points():
    points = generer_polygone_convexe(100)
    debut = time.perf_counter()

    tris = simple_triangulation(points)

    duree = time.perf_counter() - debut
    assert duree < 0.5  # 0.5 seconde
    assert len(tris) > 0


# ------------------------------------------------------------
# TESTS PERFORMANCE SERIALISATION
# ------------------------------------------------------------

@pytest.mark.perf
def test_serialisation_1000_points():
    points = [(random.random(), random.random()) for _ in range(1000)]

    debut = time.perf_counter()
    data = pointset_to_binary(points)
    pts = binary_to_pointset(data)
    duree = time.perf_counter() - debut

    assert len(pts) == len(points)
    assert duree < 0.1  # 100 ms


@pytest.mark.perf
def test_serialisation_triangles_500():
    points = [(random.random(), random.random()) for _ in range(200)]
    triangles = [(i, i + 1, i + 2) for i in range(0, 500)]

    debut = time.perf_counter()
    data = triangles_to_binary(points, triangles)
    pts2, tris2 = binary_to_triangles(data)
    duree = time.perf_counter() - debut

    assert len(tris2) == len(triangles)
    assert duree < 0.2  # 200 ms
