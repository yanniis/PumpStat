import requests

RAVEN_URL = "https://a.free.nosqlproject.ravendb.cloud/databases/prixcarburant"
CERT = ("certif/client.pem", "certif/client.key")

def get_prix_moyens():
    carburants = ["SP95", "SP98", "E10", "Gazole"]
    moyennes = {}

    for c in carburants:
        champ = f"Prix {c}"
        query = {
            "Query": f"""
                from Stations_transformees_retry_good_maybes
                where exists('{champ}') and '{champ}' != null
            """
        }
        response = requests.post(f"{RAVEN_URL}/queries", json=query, cert=CERT)
        response.raise_for_status()

        # Sécurisation complète : cast uniquement si valeur numérique
        prix = []
        for doc in response.json().get("Results", []):
            val = doc.get(champ)
            try:
                prix.append(float(val))
            except (TypeError, ValueError):
                continue

        moyenne = round(sum(prix) / len(prix), 3) if prix else None
        moyennes[c] = moyenne

    return {"moyennes": moyennes}
