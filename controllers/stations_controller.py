import requests
import json
import uuid
from collections import Counter
import os
from dotenv import load_dotenv

# URL de base RavenDB + certif
RAVEN_URL = os.getenv("RAVEN_URL")
CERT = (os.getenv("CERT_PATH"), os.getenv("KEY_PATH"))

COLLECTION_NAME = "Stations"

def read_all_stations():
    query = {
        "Query": f"from {COLLECTION_NAME}"
    }
    response = requests.post(f"{RAVEN_URL}/queries", json=query, cert=CERT)
    response.raise_for_status()
    return response.json().get("Results", [])

def create_station(data):
    new_id = f"stations/{uuid.uuid4()}"
    data = data.copy()
    if "@metadata" not in data:
        data["@metadata"] = {}
    data["@metadata"]["@collection"] = COLLECTION_NAME
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.put(
            f"{RAVEN_URL}/docs?id={new_id}",
            json=data,
            cert=CERT,
            headers=headers
        )
        response.raise_for_status()
        return new_id
    except requests.exceptions.HTTPError as e:
        print("Status code:", e.response.status_code)
        print("Response body:", e.response.text)
        raise

def read_station_by_id(station_id):
    response = requests.get(f"{RAVEN_URL}/docs?id={station_id}", cert=CERT)
    response.raise_for_status()
    doc = response.json()
    return doc.get("Results", [None])[0]

def update_station(station_id, updated_data):
    existing = read_station_by_id(station_id)
    if not existing:
        return False

    existing.update(updated_data)

    headers = {"Content-Type": "application/json"}
    response = requests.put(f"{RAVEN_URL}/docs?id={station_id}", 
                            data=json.dumps(existing), cert=CERT, headers=headers)
    response.raise_for_status()
    return True

def delete_station(station_id):
    response = requests.delete(f"{RAVEN_URL}/docs?id={station_id}", cert=CERT)
    if response.status_code == 404:
        return False
    response.raise_for_status()
    return True

def most_common_service_only():
    stations = read_all_stations()  # récupère toutes les stations via ta fonction existante

    all_services = []

    for station in stations:
        services_field = (
            station.get("services") or
            station.get("Services") or
            station.get("service") or {}
        )

        services_list = []

        if isinstance(services_field, dict):
            inner = services_field.get("service")
            if isinstance(inner, list):
                services_list = inner
            elif isinstance(inner, str):
                services_list = [inner]
        elif isinstance(services_field, list):
            services_list = services_field
        elif isinstance(services_field, str):
            services_list = [services_field]

        all_services.extend([s.strip() for s in services_list if isinstance(s, str)])

    service_counter = Counter(all_services)

    print("\n=== Service le plus proposé ===")
    if not service_counter:
        print("Aucun service trouvé.")
        return None

    most_common = service_counter.most_common(1)[0]
    print(f"Service le plus proposé : {most_common[0]} ({most_common[1]} fois)")

    return most_common