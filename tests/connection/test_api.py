from unittest.mock import patch
import pytest

from triangulator.api import app


# ---------------------------------------------------------------------------
# FIXTURE CLIENT FLASK
# ---------------------------------------------------------------------------

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ---------------------------------------------------------------------------
# HEALTH
# ---------------------------------------------------------------------------

def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json == {"status": "ok"}


# ---------------------------------------------------------------------------
# TRIANGULATE – ERREURS DE REQUÊTE
# ---------------------------------------------------------------------------

def test_triangulate_no_json(client):
    res = client.post("/triangulate")
    assert res.status_code == 400
    assert b"Aucune donnee" in res.data or b"Aucune donn" in res.data


def test_triangulate_missing_id(client):
    res = client.post("/triangulate", json={})
    assert res.status_code == 400
    assert b"pointset_id" in res.data.lower()


# ---------------------------------------------------------------------------
# TRIANGULATE – POINTSET MANAGER
# ---------------------------------------------------------------------------

@patch("triangulator.api.pointset_client.fetch_pointset")
def test_triangulate_psm_offline(mock_fetch, client):
    mock_fetch.side_effect = Exception("PSM down")

    res = client.post("/triangulate", json={"pointset_id": "123"})
    assert res.status_code == 503


# ---------------------------------------------------------------------------
# TRIANGULATE – CONVERSION BINAIRE
# ---------------------------------------------------------------------------

@patch("triangulator.api.pointset_client.fetch_pointset")
def test_triangulate_binary_to_pointset_error(mock_fetch, client):
    mock_fetch.return_value = b"invalid_binary"

    res = client.post("/triangulate", json={"pointset_id": "123"})
    assert res.status_code == 400


# ---------------------------------------------------------------------------
# TRIANGULATE – ERREUR ALGO
# ---------------------------------------------------------------------------

@patch("triangulator.api.pointset_client.fetch_pointset")
@patch("triangulator.api.simple_triangulation")
def test_triangulate_algo_error(mock_algo, mock_fetch, client):
    # pointset valide minimal (1 point)
    mock_fetch.return_value = b"\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    mock_algo.side_effect = Exception("Algo failed")

    res = client.post("/triangulate", json={"pointset_id": "123"})
    assert res.status_code == 500


# ---------------------------------------------------------------------------
# TRIANGULATE – HAPPY PATH
# ---------------------------------------------------------------------------

@patch("triangulator.api.pointset_client.fetch_pointset")
def test_triangulate_happy_path(mock_fetch, client):
    # 3 points → 1 triangle
    mock_fetch.return_value = (
        b"\x03\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x80?\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x80?"
    )

    res = client.post("/triangulate", json={"pointset_id": "123"})
    assert res.status_code == 200
    assert res.mimetype == "application/octet-stream"
    assert len(res.data) > 0


# ---------------------------------------------------------------------------
# HANDLERS D’ERREURS
# ---------------------------------------------------------------------------

def test_404_handler(client):
    res = client.get("/route/inconnue")
    assert res.status_code == 404
    assert b"route" in res.data.lower()


def test_405_handler(client):
    res = client.put("/triangulate", json={})
    assert res.status_code == 405
    assert b"autor" in res.data.lower()
