from flask import Flask
from routes.carburants import carburant_routes
from routes.regions import region_routes
from routes.stats import stats_routes
from routes.stations import stations_routes

app = Flask(__name__)

# Enregistrer les Blueprints
app.register_blueprint(carburant_routes, url_prefix="/api")
app.register_blueprint(region_routes, url_prefix="/api")
app.register_blueprint(stats_routes, url_prefix="/api")
app.register_blueprint(stations_routes, url_prefix="/api")

if __name__ == '__main__':
    app.run(debug=True)
