"""
API Flask du Triangulator.
Service responsable de récupérer un PointSet auprès du PointSetManager,
de le trianguler, puis de renvoyer la représentation binaire des triangles.
"""

from __future__ import annotations

from flask import Flask, request, jsonify, Response
import urllib.request
import urllib.error
import logging

from triangulator.serialisation import (
    binary_to_pointset,
    triangles_to_binary,
)
from triangulator.triangulation import simple_triangulation

# Logging minimal
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


# ---------------------------------------------------------------------------
#                             CLIENT POINTSETMANAGER
# ---------------------------------------------------------------------------

class PointSetManagerClient:
    """
    Client minimaliste du PointSetManager.
    Implémenté UNIQUEMENT avec la bibliothèque standard (urllib).
    """

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip("/")

    def fetch_pointset(self, pointset_id: str) -> bytes:
        url = f"{self.base_url}/pointset/{pointset_id}"
        try:
            with urllib.request.urlopen(url) as response:
                return response.read()
        except Exception as e:
            raise RuntimeError("Erreur PSM") from e


# Client global
pointset_client = PointSetManagerClient()


# ---------------------------------------------------------------------------
#                                   ENDPOINTS
# ---------------------------------------------------------------------------

@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.post("/triangulate")
def triangulate():
    # ------------------------------------------------------------------
    # CAS JSON
    # ------------------------------------------------------------------
    if request.is_json:
        payload = request.get_json(silent=True)

        if payload is None:
            return jsonify({"error": "Aucune donnée fournie"}), 400

        if "pointset_id" not in payload:
            return jsonify({"error": "pointset_id manquant"}), 400

        try:
            data = pointset_client.fetch_pointset(payload["pointset_id"])
        except Exception:
            return jsonify({"error": "Erreur PSM"}), 503

        try:
            points = binary_to_pointset(data)
        except Exception:
            return jsonify({"error": "Erreur conversion pointset"}), 400

    # ------------------------------------------------------------------
    # CAS BINAIRE DIRECT
    # ------------------------------------------------------------------
    else:
        data = request.get_data()

        if not data:
            return jsonify({"error": "Aucune donnée fournie"}), 400

        try:
            points = binary_to_pointset(data)
        except Exception:
            return jsonify({"error": "Erreur conversion pointset"}), 400

    # ------------------------------------------------------------------
    # TRIANGULATION
    # ------------------------------------------------------------------
    try:
        triangles = simple_triangulation(points)
    except Exception:
        return jsonify({"error": "Erreur triangulation"}), 500

    # ------------------------------------------------------------------
    # SERIALISATION
    # ------------------------------------------------------------------
    try:
        binary_output = triangles_to_binary(points, triangles)
    except Exception:
        return jsonify({"error": "Erreur conversion triangles"}), 500

    return Response(binary_output, mimetype="application/octet-stream"), 200


# ---------------------------------------------------------------------------
#                              HANDLERS ERREURS
# ---------------------------------------------------------------------------

@app.errorhandler(404)
def not_found(_):
    return jsonify({"error": "route non trouvee"}), 404


@app.errorhandler(405)
def method_not_allowed(_):
    return jsonify({"error": "Non autorise"}), 405


# ---------------------------------------------------------------------------
#                                  MAIN
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
