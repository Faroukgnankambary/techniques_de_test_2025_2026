from triangulator.triangulation import (
    simple_triangulation,
    bounding_triangle,
    is_point_in_triangle,
)


class TestTriangulationReal:

    def test_simple_triangle(self):
        points = [(0,0), (1,0), (0,1)]
        tris = simple_triangulation(points)
        assert tris == [(0,1,2)]

    def test_collinear_points(self):
        points = [(0,0), (1,0), (2,0)]
        tris = simple_triangulation(points)
        assert tris == []  # aucun triangle possible

    def test_square(self):
        points = [(0,0), (1,0), (1,1), (0,1)]
        tris = simple_triangulation(points)
        assert len(tris) == 2

    def test_point_in_triangle(self):
        a,b,c = (0,0),(1,0),(0,1)
        assert is_point_in_triangle((0.2,0.2), a,b,c) is True
        assert is_point_in_triangle((1,1), a,b,c) is False

    def test_bounding_triangle(self):
        pts = [(10,10)]
        a,b,c = bounding_triangle(pts)
        assert isinstance(a, tuple)
        assert isinstance(b, tuple)
        assert isinstance(c, tuple)
