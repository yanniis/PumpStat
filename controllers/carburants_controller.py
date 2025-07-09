import requests

RAVEN_URL = "https://a.free.nosqlproject.ravendb.cloud/databases/prixcarburant"
CERT = ("certif/client.pem", "certif/client.key")

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

    # Trier les résultats par prix (Valeur)
    sorted_results = sorted(all_results, key=lambda x: x["Valeur"])
    return sorted_results[:5]
