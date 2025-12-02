import triangulator.serialisation as serial
from unittest.mock import patch

class TestSerialisation:

    def test_pointset_to_binary_mock(self):
        with patch("triangulator.serialisation.pointset_to_binary") as mock:
            mock.return_value = b"donnees_mockees"
            res = serial.pointset_to_binary([(0,0)])
            assert res == b"donnees_mockees"

    def test_binary_to_pointset_mock(self):
        with patch("triangulator.serialisation.binary_to_pointset") as mock:
            mock.return_value = [(1.5, 2.5)]
            res = serial.binary_to_pointset(b"bin")
            assert res == [(1.5, 2.5)]

    def test_triangles_to_binary_mock(self):
        with patch("triangulator.serialisation.triangles_to_binary") as mock:
            mock.return_value = b"T"
            res = serial.triangles_to_binary([(0,0)], [(0,1,2)])
            assert res == b"T"

    def test_binary_to_triangles_mock(self):
        with patch("triangulator.serialisation.binary_to_triangles") as mock:
            mock.return_value = ([(0,0)], [(0,1,2)])
            pts, tris = serial.binary_to_triangles(b"bin")
            assert pts == [(0,0)]
            assert tris == [(0,1,2)]
