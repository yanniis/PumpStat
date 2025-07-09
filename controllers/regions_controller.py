import requests

RAVEN_URL = "https://a.free.nosqlproject.ravendb.cloud/databases/prixcarburant"
CERT = ("certif/client.pem", "certif/client.key")

def get_stations_by_region(code_region):
    query = {
        "Query": f"""
            from Stations_transformees_retry_good_maybes
            where code_region = '{code_region}'
            select Ville, code_departement, code_region, Prix SP95, Prix E10, Prix SP98
        """
    }
    response = requests.post(f"{RAVEN_URL}/queries", json=query, cert=CERT)
    response.raise_for_status()
    return response.json().get("Results", [])

def get_regions_disponibles():
    # Peut être remplacé par une index/map-reduce plus performante
    query = {
        "Query": """
            from Stations_transformees_retry_good_maybes
            select distinct(code_region)
        """
    }
    response = requests.post(f"{RAVEN_URL}/queries", json=query, cert=CERT)
    response.raise_for_status()
    raw = response.json().get("Results", [])
    return list({r["code_region"] for r in raw if "code_region" in r})
