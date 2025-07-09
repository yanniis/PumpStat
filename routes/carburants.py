from flask import Blueprint, jsonify
from controllers.carburants_controller import get_top5_par_carburant

carburant_routes = Blueprint("carburants", __name__)

@carburant_routes.route("/carburants/<carburant>", methods=["GET"])
def top5_endpoint(carburant):
    try:
        results = get_top5_par_carburant(carburant)
        return jsonify({"carburant": carburant, "top5": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
