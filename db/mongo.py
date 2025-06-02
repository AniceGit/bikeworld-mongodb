from pymongo import MongoClient
import json


def init_db(data) -> None:
    """Réinitialisation de la base de données

    Args:
        data (dict): dictionnaire contenant les données du fichier JSON

    """
    client = MongoClient("mongodb://localhost:27017/")

    # Récupération (ou création) d'une base de données
    db = client["bikeworld-mongo"]


    # destruction de la collection des utilisateurs
    collection = db["utilisateur"]
    print("Suppression de la collection utilisateur")
    collection.drop()

    # creation de la collection des utilisateurs
    print("Création de la collection utilisateur")
    db.create_collection("utilisateur")

    print(f"Population de la collection utilisateur")
    # Boucle pour insert les utilisateurs du fichier data.json
    utilisateurs: dict = data.get("utilisateur")
    # print(f"utilisateurs: {utilisateurs}")
    result_utilisateurs = collection.insert_many(utilisateurs)
    # print(f"IDs insérés dans la collection utilisateur: {result_utilisateurs.inserted_ids}")

    # destruction de la collection des produits
    collection = db["produit"]
    print("Suppression de la collection produit")
    collection.drop()

    # creation de la collection des produits
    print("Création de la collection produit")
    db.create_collection("produit")

    print(f"Population de la collection produit")
    # Boucle pour insert les produits du fichier data.json
    produits: dict = data.get("produit")
    result_produits = collection.insert_many(produits)
    # print(f"IDs insérés dans la collection produit: {result_produits.inserted_ids}")



    # destruction de la collection des commandes
    collection = db["commande"]
    print("Suppression de la collection commande")
    collection.drop()

    # creation de la collection des commandes
    print("Création de la collection commande")
    db.create_collection("commande")

    collection = db["commande"]
    print(f"Population de la collection commande")
    # Boucle pour insert les commandes du fichier data.json
    commandes: dict = data.get("commande")
    for commande in commandes:
        value = commande["id_utilisateur"]
        commande["id_utilisateur"] = result_utilisateurs.inserted_ids[value - 1]
        # print(f"id utilisateur à insérer: {commande["id_utilisateur"]} / values: {value}")
        produit_commandes: dict = commande.get("produit_commande")
        for produit_commande in produit_commandes:
            value = produit_commande["id_produit"]
            produit_commande["id_produit"] = result_produits.inserted_ids[value - 1]
            # récupération des données du produit
            collection_produit = db["produit"]
            produit = collection_produit.find_one({"_id": result_produits.inserted_ids[value - 1]})
            produit_commande["nom"] = produit["nom"]
            produit_commande["desc"] = produit["desc"]
            produit_commande["spec_tech"] = produit["spec_tech"]
            produit_commande["couleur"] = produit["couleur"]
            produit_commande["image"] = produit["image"]
            # print(f"id produit à insérer: {produit_commande["id_produit"]} / values: {value}")

    result_commandes = collection.insert_many(commandes)
    # print(f"IDs insérés dans la collection commande: {result_commandes.inserted_ids}")



def lirejson(fichier: str) -> dict:
    """Lecture du fichier JSON contenant les données

    Args:
        fichier (str): URI vers le fichier JSON contenant les données

    Returns:
        dict: contenu du fichier de données sous forme de dictionnaire
    """
    data = {}
    with open(fichier, "r", encoding="utf-8") as fic:
        data = json.load(fic)

    return data


entree = input(
    "Attention! Ce script va reinitialiser la base de donnees. Continuer (O/N)"
)
if entree.upper() == "O":
    data = lirejson("db/data.json")
    init_db(data)

