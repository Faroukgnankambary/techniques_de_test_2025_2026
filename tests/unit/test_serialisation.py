import pytest
from triangulator.serialisation import (
    pointset_to_binary,
    binary_to_pointset,
    triangles_to_binary,
    binary_to_triangles,
)


class TestSerialisationReal:

    def test_pointset_roundtrip(self):
        points = [(0.0, 1.0), (2.5, -3.75)]
        data = pointset_to_binary(points)
        decoded = binary_to_pointset(data)
        assert decoded == points

    def test_empty_pointset(self):
        points = []
        data = pointset_to_binary(points)
        decoded = binary_to_pointset(data)
        assert decoded == []

    def test_triangles_roundtrip(self):
        points = [(0, 0), (1, 0), (0, 1)]
        triangles = [(0, 1, 2)]

        data = triangles_to_binary(points, triangles)
        pts2, tris2 = binary_to_triangles(data)

        assert pts2 == points
        assert tris2 == triangles

    def test_invalid_binary_pointset(self):
        with pytest.raises(Exception):
            binary_to_pointset(b"\x00\x01")  # Données absurdes

    def test_invalid_binary_triangles(self):
        with pytest.raises(Exception):
            binary_to_triangles(b"\x05\x00\x00\x99")
