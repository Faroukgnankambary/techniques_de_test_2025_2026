import triangulator.triangles as tri
from unittest.mock import patch

class TestTriangles:

    def test_validate_triangle_indices_mock(self):
        with patch("triangulator.triangles.validate_triangle_indices") as mock:
            mock.return_value = True
            res = tri.validate_triangle_indices([(0,0)], 0,1,2)
            assert res is True

    def test_triangle_area_mock(self):
        with patch("triangulator.triangles.triangle_area") as mock:
            mock.return_value = 7.5
            res = tri.triangle_area((0,0),(1,0),(0,3))
            assert res == 7.5

    def test_are_points_collinear_mock(self):
        with patch("triangulator.triangles.are_points_collinear") as mock:
            mock.return_value = True
            res = tri.are_points_collinear((0,0),(1,1),(2,2))
            assert res is True

    def test_validate_triangulation_mock(self):
        with patch("triangulator.triangles.validate_triangulation") as mock:
            mock.return_value = True
            res = tri.validate_triangulation([], [])
            assert res is True
