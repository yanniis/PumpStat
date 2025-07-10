from flask import json
import requests
import os
from dotenv import load_dotenv
from controllers.stations_controller import read_all_stations

RAVEN_URL = os.getenv("RAVEN_URL")
CERT = (os.getenv("CERT_PATH"), os.getenv("KEY_PATH"))

def get_top5_par_carburant(nom_carburant):
    nom_carburant = nom_carburant.lower()

    query = {
        "Query": f"""
            from Prix_des_carburants_en_france_flux_instantane_v2s as doc
            where any prix in doc.prix satisfies prix['@nom'] = '{nom_carburant}' and prix['@valeur'] != null
            select {{
                Ville: doc.Ville,
                Region: doc.code_region,
                Departement: doc.code_departement,
                Valeur: double.parse(first(doc.prix[x => x['@nom'] = '{nom_carburant}']).['@valeur'])
            }}
        """
    }

    res = requests.post(f"{RAVEN_URL}/queries", json=query, cert=CERT)
    res.raise_for_status()
    all_results = res.json().get("Results", [])

    sorted_results = sorted(all_results, key=lambda x: x["Valeur"])
    return sorted_results[:5]

# Fonction pour récupérer la liste des carburants disponibles
def get_liste_carburants_disponibles():
    query = {
        "Query": "from stations select prix"
    }
    response = requests.post(f"{RAVEN_URL}/queries", json=query, cert=CERT)
    response.raise_for_status()
    results = response.json().get("Results", [])

    carburants = set()
    for station in results:
        prix_raw = station.get("prix")
        if not prix_raw:
            continue
        try:
            prix_json = json.loads(prix_raw) if isinstance(prix_raw, str) else prix_raw
            for p in prix_json:
                nom = p.get("@nom")
                if nom:
                    carburants.add(nom)
        except Exception:
            continue

    return sorted(carburants)

def count_stations_par_carburant_avec_pourcentage():
    carburants = ["E10", "E85", "GPLc", "Gazole", "SP95", "SP98"]
    stations = read_all_stations()
    total_stations = len(stations)
    counts = {c: 0 for c in carburants}

    for s in stations:
        dispo = s.get("Carburants disponibles")
        if not dispo or not isinstance(dispo, str):
            continue  

        dispo_lower = dispo.lower()
        for c in carburants:
            if c.lower() in dispo_lower:
                counts[c] += 1

    result = {
        c: {
            "count": counts[c],
            "percentage": round(100 * counts[c] / total_stations, 2)
        }
        for c in sorted(counts, key=counts.get)
    }
    return result
