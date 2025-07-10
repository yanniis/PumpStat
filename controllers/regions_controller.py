import requests
import os
from dotenv import load_dotenv

RAVEN_URL = os.getenv("RAVEN_URL")
CERT = (os.getenv("CERT_PATH"), os.getenv("KEY_PATH"))

def get_stations_by_region(code_region):
    query = {
        "Query": f"""
            from stations
            where code_region = '{code_region}'
            select Ville, code_departement, code_region, Prix SP95, Prix E10, Prix SP98
        """
    }
    response = requests.post(f"{RAVEN_URL}/queries", json=query, cert=CERT)
    response.raise_for_status()
    return response.json().get("Results", [])

def get_regions_disponibles():
    query = {
        "Query": """
            from stations
            select distinct(code_region)
        """
    }
    response = requests.post(f"{RAVEN_URL}/queries", json=query, cert=CERT)
    response.raise_for_status()
    raw = response.json().get("Results", [])
    return list({r["code_region"] for r in raw if "code_region" in r})

def region_with_most_services():
    query = {
        "Query": "from stations select code_region, services"
    }
    response = requests.post(f"{RAVEN_URL}/queries", json=query, cert=CERT)
    response.raise_for_status()
    stations = response.json().get("Results", [])
    
    services_by_region = {}
    for station in stations:
        region = station.get("code_region", "Inconnue")
        services_field = station.get("services") or station.get("Services") or station.get("service") or []
        if isinstance(services_field, dict):
            possible_service = services_field.get("service", [])
            if isinstance(possible_service, list):
                services_list = possible_service
            elif isinstance(possible_service, str):
                services_list = [possible_service]
            else:
                services_list = []
        elif isinstance(services_field, list):
            services_list = services_field
        elif isinstance(services_field, str):
            services_list = [services_field]
        else:
            services_list = []

        count = len(services_list)
        services_by_region[region] = services_by_region.get(region, 0) + count

    if not services_by_region:
        return None

    sorted_regions = sorted(services_by_region.items(), key=lambda x: x[1], reverse=True)
    top_region, top_count = sorted_regions[0]
    return top_region, top_count


def region_with_lowest_prices():
    query = {
       "Query": """
            from stations as s
            select {
                code_region: s.code_region,
                prix_gazole: s['Prix Gazole'],
                prix_sp95: s['Prix SP95'],
                prix_sp98: s['Prix SP98']
            }
        """
    }
    response = requests.post(f"{RAVEN_URL}/queries", json=query, cert=CERT)
    response.raise_for_status()
    stations = response.json().get("Results", [])

    min_price_gazole = {}
    min_price_sp95 = {}
    min_price_sp98 = {}

    for station in stations:
        region = station.get("code_region") or "Inconnue"

        try:
            gazole = station.get("prix_gazole")
            gazole = float(gazole)
            if gazole > 0:
                if region not in min_price_gazole or gazole < min_price_gazole[region]:
                    min_price_gazole[region] = gazole
        except (TypeError, ValueError):
            continue

        try:
            sp95 = station.get("prix_sp95")
            sp95 = float(sp95)
            if sp95 > 0:
                if region not in min_price_sp95 or sp95 < min_price_sp95[region]:
                    min_price_sp95[region] = sp95
        except (TypeError, ValueError):
            continue

        try:
            sp98 = station.get("prix_sp98")
            sp98 = float(sp98)
            if sp98 > 0:
                if region not in min_price_sp98 or sp98 < min_price_sp98[region]:
                    min_price_sp98[region] = sp98
        except (TypeError, ValueError):
            continue

    def get_best_price(price_dict):
        if not price_dict:
            return None
        best_region, best_price = sorted(price_dict.items(), key=lambda x: x[1])[0]
        return {"region": best_region, "price": best_price}

    return {
        "Gazole": get_best_price(min_price_gazole),
        "SP95": get_best_price(min_price_sp95),
        "SP98": get_best_price(min_price_sp98),
    }


