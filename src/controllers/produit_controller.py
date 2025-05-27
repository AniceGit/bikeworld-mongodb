import sqlite3
from models.produit import Produit


def get_produits() -> list[Produit]:
    """
    Récupère tous les produits de la base de données.

    Returns:
        list[Produit]: Une liste d'objets Produit représentant tous les produits disponibles.

    Raises:
        Exception: Si aucun produit n'est trouvé dans la base de données.
    """

    lignes = []
    with sqlite3.connect("bikeworld.db") as conn:
        cur = conn.cursor()
        cur.execute(
            """ \
                    SELECT id,
                        nom,
                        desc,
                        spec_tech, 
                        couleur, 
                        image, 
                        prix, 
                        stock,
                        ventes,
                        actif
                    FROM produit 
                """
        )
        result = cur.fetchall()
        if result is None:
            raise Exception(f"Aucun articles")

        for id, nom, desc, spec_tech, couleur, image, prix, stock, ventes, actif in result:
            lignes.append(
                Produit(id, nom, desc, spec_tech, couleur, image, prix, stock, ventes, actif)
            )
    return lignes


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

    with sqlite3.connect("bikeworld.db") as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, nom, desc, spec_tech, couleur, image, prix, stock, ventes, actif
            FROM produit
            WHERE id = ?
        """,
            (id_produit,),
        )
        result = cur.fetchone()

        if not result:
            raise Exception("Produit non trouvé")

        id, nom, desc, spec_tech, couleur, image, prix, stock, ventes, actif = result
        produit = Produit(id, nom, desc, spec_tech, couleur, image, prix, stock, ventes, actif)
        return produit


def get_top_3_ventes() -> list[Produit]:
    """
    Récupère les trois produits les plus vendus.

    Returns:
        list[Produit]: Une liste d'objets Produit représentant les trois produits les plus vendus.

    Raises:
        Exception: Si aucun produit n'est trouvé dans la base de données.
    """

    with sqlite3.connect("bikeworld.db") as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT id, nom, desc, spec_tech, couleur, image, prix, stock, ventes, actif
                FROM produit
                WHERE actif = 1
                ORDER BY ventes DESC
                LIMIT 3
            """
            )
    result = cur.fetchall()
    if not result:
        raise Exception("Produit non trouvé")

    produits = []
    for id, nom, desc, spec_tech, couleur, image, prix, stock, ventes, actif in result:
        produits.append(
            Produit(id, nom, desc, spec_tech, couleur, image, prix, stock, ventes, actif)
        )
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
        
    with sqlite3.connect("bikeworld.db") as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT nom
            FROM produit
            WHERE id = :id_produit
        """,
            {"id_produit": id_produit},
        )
        result = cur.fetchone()
        if not result:
            raise Exception("Produit non trouvé")
        nom_produit = result
        return nom_produit

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
    
    with sqlite3.connect("bikeworld.db") as conn:
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE produit
            SET nom = :nom,
                desc = :desc,
                spec_tech = :spec_tech,
                couleur = :couleur,
                image = :image,
                prix = :prix,
                stock = :stock,
                actif = :actif
            WHERE id = :id
        """,
            {"id": id, "nom": nom, "desc": description, "spec_tech": spec_tech, "couleur": couleur, "image": image, "prix": prix, "stock": stock, "actif" :actif},
        )
