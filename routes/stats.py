from flask import Blueprint, jsonify
from controllers.stats_controller import get_prix_moyens

stats_routes = Blueprint('stats_routes', __name__)

@stats_routes.route('/stats/prix-moyen', methods=['GET'])
def prix_moyen():
    try:
        return jsonify(get_prix_moyens())
    except Exception as e:
        return jsonify({"error": str(e)}), 500
