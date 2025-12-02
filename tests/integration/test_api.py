"""
Tests d’intégration de l’API avec mocks.
"""

from unittest.mock import patch
import json
import pytest
from triangulator.api import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json["status"] == "ok"


@patch("triangulator.api.triangles_to_binary")
@patch("triangulator.api.simple_triangulation")
@patch("triangulator.api.binary_to_pointset")
def test_triangulate_json(mock_pts, mock_algo, mock_bin, client):
    mock_pts.return_value = [(0,0),(1,0),(0,1)]
    mock_algo.return_value = [(0,1,2)]
    mock_bin.return_value = b"BIN"

    res = client.post("/triangulate", json={"pointset_id": "123"})

    assert res.status_code == 200
    assert res.data == b"BIN"
