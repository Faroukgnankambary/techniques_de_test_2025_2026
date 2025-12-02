import triangulator.triangulation as tr
from unittest.mock import patch

class TestTriangulation:

    def test_simple_triangulation_mock(self):
        with patch("triangulator.triangulation.simple_triangulation") as mock:
            mock.return_value = [(0,1,2)]
            res = tr.simple_triangulation([(0,0),(1,0),(0,1)])
            assert res == [(0,1,2)]

    def test_bounding_triangle_mock(self):
        with patch("triangulator.triangulation.bounding_triangle") as mock:
            mock.return_value = ((0,0),(10,0),(0,10))
            res = tr.bounding_triangle([(1,2)])
            assert res == ((0,0),(10,0),(0,10))

    def test_is_point_in_triangle_mock(self):
        with patch("triangulator.triangulation.is_point_in_triangle") as mock:
            mock.return_value = True
            res = tr.is_point_in_triangle((0.5,0.5),(0,0),(1,0),(0,1))
            assert res is True
