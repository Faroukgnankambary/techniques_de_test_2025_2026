from flask import Flask, jsonify, request, Response

app = Flask(__name__)

# stubs mockables
def binary_to_pointset(data): pass
def simple_triangulation(points): pass
def triangles_to_binary(points, triangles): pass


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/triangulate", methods=["POST"])
def triangulate():
    # juste un squelette pour que les tests puissent mocker
    content = request.get_json()
    if not content or "pointset_id" not in content:
        return jsonify({"error": "missing id"}), 400

    # les appels internes seront mockés donc c'est très bien
    pts = binary_to_pointset(b"")
    tris = simple_triangulation(pts)
    binaire = triangles_to_binary(pts, tris)
    return Response(binaire, content_type="application/octet-stream")
