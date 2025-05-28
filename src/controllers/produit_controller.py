import pymongo
from src.models.produit import Produit

#Connexion à MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["bikeworld-mongo"]  
collection = db["produit"]

def get_produits() -> list[Produit]:
    """
    Récupère tous les produits de la base de données.

    Returns:
        list[Produit]: Une liste d'objets Produit représentant tous les produits disponibles.

    Raises:
        Exception: Si aucun produit n'est trouvé dans la base de données.
    """

    produits = []
    result = collection.find({})
    if result is None:
            raise Exception(f"Aucun article")
    
    for produit in result:
        if "_id" not in produit:
            raise Exception(f"il manque un id dans le document")
        produits.append(
            Produit(
                  produit["_id"],
                  produit["nom"],
                  produit["desc"],
                  produit["spec_tech"],
                  produit["couleur"],
                  produit["image"],
                  produit["prix"],
                  produit["stock"],
                  produit["ventes"],
                  produit["actif"],))
    return produits


def get_details_produit(id_produit: int) -> Produit:
    """
    Récupère les détails d'un produit spécifique à partir de son identifiant.

    Args:
        id_produit (int): L'identifiant du produit à récupérer.

    Returns:
        Produit: Un objet Produit contenant les détails du produit.

    Raises:
        Exception: Si le produit n'est pas trouvé dans la base de données.
    """

    result = collection.find_one({"_id":id_produit})
    if result is None:
            raise Exception(f"Aucun articles")
    produit = Produit(
                result["_id"],
                result["nom"],
                result["desc"],
                result["spec_tech"],
                result["couleur"],
                result["image"],
                result["prix"],
                result["stock"],
                result["ventes"],
                result["actif"]  
    )
    return produit


def get_top_3_ventes() -> list[Produit]:
    """
    Récupère les trois produits les plus vendus.

    Returns:
        list[Produit]: Une liste d'objets Produit représentant les trois produits les plus vendus.

    Raises:
        Exception: Si aucun produit n'est trouvé dans la base de données.
    """

    result = collection.find({"actif":1}).sort("ventes",-1).limit(3)
    if not result:
        raise Exception("Produit non trouvé")
    
    produits = []
     
    for produit in result:
        produits.append(
            Produit(
                produit["_id"],
                produit["nom"],
                produit["nom"],
                produit["spec_tech"],
                produit["couleur"],
                produit["image"],
                produit["prix"],
                produit["stock"],
                produit["ventes"],
                produit["actif"],))
    return produits


def get_produit_nom_by_id(id_produit: int) -> str:
    """
    Récupère le nom d'un produit à partir de son identifiant.

    Args:
        id_produit (int): L'identifiant du produit.

    Returns:
        str: Le nom du produit.

    Raises:
        Exception: Si le produit n'est pas trouvé dans la base de données.
    """
    result = collection.find_one({"_id":id_produit},{"nom":1})
    if not result:
        raise Exception("Produit non trouvé")
    return result["nom"]


def modifier_produit(id, nom, description, spec_tech, couleur, image, prix, stock, actif):
    """
    Modifie les détails d'un produit dans la base de données.

    Args:
        id (int): L'identifiant du produit à modifier.
        nom (str): Le nouveau nom du produit.
        description (str): La nouvelle description du produit.
        spec_tech (str): Les nouvelles spécifications techniques du produit.
        couleur (str): La nouvelle couleur du produit.
        image (str): Le nouveau chemin de l'image du produit.
        prix (float): Le nouveau prix du produit.
        stock (int): Le nouveau niveau de stock du produit.
        actif (int): L'état actif du produit (1 pour actif, 0 pour inactif).
    """
    
    update_data = {
            "nom": nom,
            "desc": description,
            "spec_tech": spec_tech,
            "couleur": couleur,
            "image": image,
            "prix": prix,
            "stock": stock,
            "actif": actif
        }
    
    collection.update_one({"_id":id},{"$set":update_data})