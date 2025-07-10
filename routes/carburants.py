from flask import Blueprint, jsonify
from controllers.carburants_controller import get_top5_par_carburant
from controllers.carburants_controller import get_liste_carburants_disponibles
from controllers.carburants_controller import count_stations_par_carburant_avec_pourcentage

carburant_routes = Blueprint("carburants", __name__)

@carburant_routes.route("/carburants/<carburant>", methods=["GET"])
def top5_endpoint(carburant):
    try:
        results = get_top5_par_carburant(carburant)
        return jsonify({"carburant": carburant, "top5": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@carburant_routes.route("/carburants", methods=["GET"])
def liste_carburants_endpoint():
    try:
        carburants = get_liste_carburants_disponibles()
        return jsonify({"carburants": carburants})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
@carburant_routes.route("/carburants/count", methods=["GET"])
def count_stations_carburants_endpoint():
    try:
        result = count_stations_par_carburant_avec_pourcentage()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500