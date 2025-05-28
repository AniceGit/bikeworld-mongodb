import streamlit as st
from pymongo import MongoClient
from typing import Any, Dict
from src.models.commande import Commande
from src.models.adresse import Adresse
from src.models.utilisateur import Utilisateur
from src.models.panier import Panier
from src.models.produit_commande import ProduitCommande


def supprimer_commande(id_commande: int) -> None:
    """
    Supprime une commande avec son id dans la base de données.

    Args:
        id (int): Identifiant de la commande à supprimer

    Returns:
        None: 
    """
    # Connexion au serveur MongoDB local
    client = MongoClient("mongodb://localhost:27017/")
    db = client["bikeworld-mongo"]

    collection = db["commande"]

    collection.deleteOne({"_id": id_commande})



def get_commandes_by_utilisateur(id_utilisateur: str) -> list[Commande] | None:
    """
    Récupère toutes les commandes de l'utilisateur passé en paramètre.

    Args:
        id (int): Identifiant de l'utilisateur

    Returns:
        list[Commande] | None : liste des commandes de l'utilisateur
    """
    # Connexion au serveur MongoDB local
    client = MongoClient("mongodb://localhost:27017/")
    db = client["bikeworld-mongo"]

    collection = db["commande"]

    commandes = []
    for commande in collection.find({"id_utilisateur": id_utilisateur}):
        adresse = commande["adresse"]
        mon_adresse = Adresse(0, adresse["numero"], adresse["type_voie"], adresse["nom_voie"], adresse["code_postal"], adresse["ville"], adresse["pays"], 0, 0, 0)

        ma_commande = Commande(commande["_id"], commande["date_commande"], commande["etat"], commande["prix_total"], commande["frais_livraison"], commande["id_utilisateur"])
        ma_commande.id_adresse = mon_adresse
        lignes = []
        cpt = 0
        for ligne in commande["produit_commande"]:
            cpt += 1
            ma_ligne = ProduitCommande(cpt, ligne["quantite"], ligne["prix"], ligne["id_produit"], ma_commande.id)
            lignes.append(ma_ligne)
        commandes.append(ma_commande)

    return commandes


# Deprecated
def get_adresse_commande(id_adresse: int) -> Adresse | None:
    """
    Deprecated
    Récupère l'adresse de la commande passée en paramètre.

    Args:
        id (int): Identifiant de la commande

    Returns:
        Adresse | None: adresse utilisée pour la commande
    """
    adresse_commande = None
    with sqlite3.connect("bikeworld.db") as conn:
        cur = conn.cursor()

        cur.execute(
            """
                SELECT id,
                    numero,
                    type_voie,
                    nom_voie,
                    code_postal,
                    ville,
                    pays,
                    defaut,
                    active,
                    id_utilisateur
                FROM adresse WHERE id = :id_adresse
            """,
            {"id_adresse": id_adresse},
        )

        result = cur.fetchone()

        if result is None:
            raise Exception(f"Adresse de la commande {id_adresse} introuvable.")

        (
            id,
            numero,
            type_voie,
            nom_voie,
            code_postal,
            ville,
            pays,
            defaut,
            active,
            id_utilisateur,
        ) = result
        adresse_commande = Adresse(
            id,
            numero,
            type_voie,
            nom_voie,
            code_postal,
            ville,
            pays,
            defaut,
            active,
            id_utilisateur,
        )

    return adresse_commande


def transformer_panier() -> bool:
    """
    Transformation du panier en commande.

    Args:

    Returns:
        None: 
    """
    panier: Panier = st.session_state.panier


    user:Utilisateur = st.session_state["utilisateur"]
    if user.adresse is None:
        return False


    commande = dict()
    commande["date_commande"] = panier.date_panier
    commande["etat"] =  "Validee"
    commande["prix_total"] = panier.total_panier
    commande["frais_livraison"] = panier.frais_livraison

    ma_ligne = dict()
    for pc in panier.liste_produits_quantite:
        ma_ligne["quantite"] = pc.quantie
        ma_ligne["prix"] = pc.prix
        ma_ligne["id_produit"] = pc.id_produit
        ma_ligne["nom"] = pc.nom
        ma_ligne["desc"] = pc.desc
        ma_ligne["spec_tech"] = pc.spec_tech
        ma_ligne["couleur"] = pc.couleur
        ma_ligne["image"] = pc.image

        commande["produit_commande"].append(ma_ligne)
    
    commande["id_utilisateur"] = panier["utilisateur"].id

    adresse = panier["adresse"]

    mon_adresse = dict()
    mon_adresse["numero"] = adresse.numero
    mon_adresse["type_voie"] = adresse.type_voie
    mon_adresse["nom_voie"] = adresse.nom_voie
    mon_adresse["code_postal"] = adresse.code_postal
    mon_adresse["ville"] = adresse.ville
    mon_adresse["pays"] = adresse.pays

    commande["id_adresse"] = mon_adresse

    print(f"Commande: {commande}")

    client = MongoClient("mongodb://localhost:27017/")

    # Récupération (ou création) d'une base de données
    db = client["bikeworld-mongo"]


    # destruction de la collection des utilisateurs
    collection = db["commande"]
    result_commandes = collection.insert_one(commande)

    return True


def get_commandes() -> list[Commande]:
    """
    Récupération de toutes les commandes.

    Args:

    Returns:
        list[Commande] | None: liste de toutes commandes (mode admin) 
    """
    # Connexion au serveur MongoDB local
    client = MongoClient("mongodb://localhost:27017/")
    db = client["bikeworld-mongo"]

    collection = db["commande"]

    commandes = []
    for commande in collection.find():
        adresse = commande["adresse"]
        mon_adresse = Adresse(0, adresse["numero"], adresse["type_voie"], adresse["nom_voie"], adresse["code_postal"], adresse["ville"], adresse["pays"], 0, 0, 0)

        ma_commande = Commande(commande["_id"], commande["date_commande"], commande["etat"], commande["prix_total"], commande["frais_livraison"], commande["id_utilisateur"])
        ma_commande.id_adresse = mon_adresse
        lignes = []
        cpt = 0
        for ligne in commande["produit_commande"]:
            cpt += 1
            ma_ligne = ProduitCommande(cpt, ligne["quantite"], ligne["prix"], ligne["id_produit"], ma_commande.id)
            lignes.append(ma_ligne)
        commandes.append(ma_commande)

    return commandes



def modifier_etat_commande(id_commande: int, etat: str) -> int | None:
    """
    Modification de l'état de la commande avec l'état passé en paramètre.

    Args:
        id (int): identifiant de la commande à modifier
        etat (str): Nouvel état de la commande
    
    Returns:
        
    """
    # Connexion au serveur MongoDB local
    client = MongoClient("mongodb://localhost:27017/")
    db = client["bikeworld-mongo"]

    collection = db["commande"]

    collection.update_one({"_id": id_commande}, {"$set": {"etat": etat}})

