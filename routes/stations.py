from flask import Blueprint, jsonify, request
from controllers.stations_controller import (
    read_all_stations,
    create_station,
    read_station_by_id,
    update_station,
    delete_station,
    most_common_service_only
)

stations_routes = Blueprint('stations_routes', __name__)

@stations_routes.route('/stations', methods=['GET'])
def get_stations():
    try:
        stations = read_all_stations()
        return jsonify(stations)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@stations_routes.route('/stations/<path:id>', methods=['GET'])
def get_station(id):
    try:
        station = read_station_by_id(id)
        if not station:
            return jsonify({"error": "Station non trouvée"}), 404
        return jsonify(station)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@stations_routes.route('/stations', methods=['POST'])
def create():
    try:
        data = request.get_json()
        station_id = create_station(data)
        if station_id:
            return jsonify({"message": "Station créée", "id": station_id}), 201
        return jsonify({"error": "Création échouée"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@stations_routes.route('/stations/<path:id>', methods=['PUT'])
def update(id):
    try:
        updated_data = request.get_json()
        success = update_station(id, updated_data)
        if not success:
            return jsonify({"error": "Station non trouvée"}), 404
        return jsonify({"message": "Station mise à jour"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@stations_routes.route('/stations/<path:id>', methods=['DELETE'])
def delete(id):
    try:
        success = delete_station(id)
        if not success:
            return jsonify({"error": "Station non trouvée"}), 404
        return jsonify({"message": "Station supprimée"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@stations_routes.route('/stations/most-common-service', methods=['GET'])
def get_most_common_service():
    try:
        result = most_common_service_only()
        if not result:
            return jsonify({"message": "Aucun service trouvé"}), 404
        return jsonify({
            "service": result[0],
            "count": result[1]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500