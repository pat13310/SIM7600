FRENCH_OPERATORS_MNC = {
    "01": "Orange",
    "02": "Orange",
    "03": "MobiquiThings",
    "04": "Sisteer",
    "05": "Globalstar Europe",
    "06": "Globalstar Europe",
    "07": "Globalstar Europe",
    "08": "SFR",
    "09": "SFR",
    "10": "SFR",
    "11": "SFR",
    "13": "SFR",
    "14": "RFF",
    "15": "Free Mobile",
    "16": "Free Mobile",
    "20": "Bouygues Telecom",
    "21": "Bouygues Telecom",
    "23": "Lebara Mobile",
    "24": "MobiquiThings",
    "25": "Lycamobile",
    "26": "Euro-Information Telecom (NRJ Mobile)",
    "27": "Coriolis Télécom",
    "28": "Airbus Defence and Space SAS",
    "29": "Cubic Telecom France",
    "30": "Syma Mobile",
    "31": "Vectone Mobile",
    "32": "Mundio Mobile",
    "33": "Felixia",
    "34": "Senion",
    "35": "La Poste Mobile",
    "36": "Legos",
    "37": "Save",
    "38": "Halys",
    "87": "Saint-Martin Mobiles",
    "88": "Bouygues Telecom",
    "89": "Italie Telecom",
    "90": "Images & Réseaux",
    "91": "Orange Caraïbe",
    "92": "ProximusMobility France",
    "93": "Thales Communications & Security SAS"
}


def get_operators_by_name(name):
    """
    Récupère la liste des opérateurs dont le nom contient la chaîne spécifiée.
    La recherche est insensible à la casse et aux accents.

    :param name: Nom ou partie du nom de l'opérateur à rechercher
    :return: Liste de tuples (mnc, nom_complet) des opérateurs correspondants
    """
    import unicodedata

    def remove_accents(input_str):
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

    name_normalized = remove_accents(name.lower())

    results = []
    for mnc, operator in FRENCH_OPERATORS_MNC.items():
        operator_normalized = remove_accents(operator.lower())
        if name_normalized in operator_normalized:
            results.append((mnc, operator))

    return results


# Exemples d'utilisation
print(get_operators_by_name("Lebara"))
