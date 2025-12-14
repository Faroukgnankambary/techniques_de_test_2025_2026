from triangulator.triangles import (
    triangle_area,
    are_points_collinear,
    validate_triangle_indices,
    validate_triangulation,
)


class TestTrianglesReal:

    def test_triangle_area(self):
        assert triangle_area((0,0), (4,0), (0,3)) == 6.0  # triangle classique

    def test_collinear(self):
        assert are_points_collinear((0,0), (1,1), (2,2)) is True
        assert are_points_collinear((0,0), (1,0), (1,1)) is False

    def test_indices_validation(self):
        points = [(0,0), (1,0), (0,1)]

        assert validate_triangle_indices(points, 0, 1, 2) is True
        assert validate_triangle_indices(points, 0, 1, 5) is False

    def test_validate_triangulation(self):
        pts = [(0,0), (1,0), (0,1)]
        tris = [(0,1,2)]
        assert validate_triangulation(pts, tris) is True
