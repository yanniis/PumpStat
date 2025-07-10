from flask import Blueprint, jsonify
from controllers.regions_controller import get_stations_by_region, get_regions_disponibles, region_with_most_services, region_with_lowest_prices

region_routes = Blueprint('region_routes', __name__)

# Toutes les régions connues (distincts)
@region_routes.route('/regions', methods=['GET'])
def regions_list():
    try:
        return jsonify(get_regions_disponibles())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Stations d'une région spécifique
@region_routes.route('/regions/<code_region>', methods=['GET'])
def stations_region(code_region):
    try:
        return jsonify(get_stations_by_region(code_region))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@region_routes.route('/regions/region-most-services', methods=['GET'])
def get_region_most_services():
    try:
        result = region_with_most_services()
        if result:
            region, total = result
            return jsonify({"region": region, "total_services": total})
        else:
            return jsonify({"error": "No data found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@region_routes.route('/regions/region-lowest-prices', methods=['GET'])
def get_region_lowest_prices():
    try:
        result = region_with_lowest_prices()
        if result:
            return jsonify(result)
        else:
            return jsonify({"error": "No data found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500