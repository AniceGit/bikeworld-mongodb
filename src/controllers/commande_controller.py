import streamlit as st
import sqlite3
from pymongo import MongoClient
from typing import Any, Dict
from bson import ObjectId
from src.models.commande import Commande
from src.models.adresse import Adresse
from src.models.utilisateur import Utilisateur
from src.models.produit import Produit
from src.models.panier import Panier
from src.models.produit_commande import ProduitCommande


def supprimer_commande(id_commande: str) -> None:
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

    collection.delete_one({"_id": ObjectId(id_commande)})



def get_commandes_by_utilisateur(id_utilisateur: ObjectId) -> list[Commande] | None:
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
    for commande in collection.find({"id_utilisateur": ObjectId(id_utilisateur)}):
        # print(f"commande: {commande}")
        adresse = commande["adresse"]
        mon_adresse = Adresse(adresse["numero"], adresse["type_voie"], adresse["nom_voie"], adresse["code_postal"], adresse["ville"], adresse["pays"], 0, 0)

        ma_commande = Commande(commande["_id"], commande["date_commande"], commande["etat"], commande["prix_total"], commande["frais_livraison"], commande["id_utilisateur"])
        ma_commande.adresse = mon_adresse
        lignes = []
        cpt = 0
        for ligne in commande["produit_commande"]:
            cpt += 1
            ma_ligne = ProduitCommande(cpt, ligne["quantite"], ligne["prix"], ligne["id_produit"], ligne["nom"], ligne["desc"], ligne["spec_tech"], ligne["couleur"], ligne["image"])
            lignes.append(ma_ligne)
        ma_commande.liste_produit_commande = lignes
        commandes.append(ma_commande)

    return commandes


def transformer_panier() -> bool:
    """
    Transformation du panier en commande.

    Args:

    Returns:
        None: 
    """
    panier: Panier = st.session_state.panier
    # print(f"Panier: {panier}")

    user:Utilisateur = st.session_state["utilisateur"]
    if user.adresses is None:
        return False


    commande = dict()
    commande["date_commande"] = panier.date_panier
    commande["etat"] =  "Validee"
    commande["prix_total"] = panier.total_panier
    commande["frais_livraison"] = panier.frais_livraison
    commande["produit_commande"] = []

    ma_ligne = dict()
    for pc in panier.liste_produits_quantite:
        # print(f"pc: {pc}")
        ma_ligne["quantite"] = pc.get("quantite")
        ma_ligne["prix"] = pc.get("prix")
        ma_ligne["id_produit"] = pc.get("produit_id")
        ma_ligne["nom"] = pc.get("produit")
        ma_ligne["desc"] = pc.get("desc")
        ma_ligne["spec_tech"] = pc.get("spec_tech")
        ma_ligne["couleur"] = pc.get("couleur")
        ma_ligne["image"] = pc.get("image")

        commande["produit_commande"].append(ma_ligne)

    commande["id_utilisateur"] = user.id
    # print(f"session user adresse: {user.adresses}")
    for adresse in user.adresses:
        if adresse.defaut == 1:
            # print(f"adresse par défaut: {adresse}")
            break

    mon_adresse = dict()
    mon_adresse["numero"] = adresse.numero
    mon_adresse["type_voie"] = adresse.type_voie
    mon_adresse["nom_voie"] = adresse.nom_voie
    mon_adresse["code_postal"] = adresse.code_postal
    mon_adresse["ville"] = adresse.ville
    mon_adresse["pays"] = adresse.pays

    commande["adresse"] = mon_adresse

    # print(f"Commande: {commande}")

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
        print(f"Ma commande: {commande}")
        adresse = commande["adresse"]
        mon_adresse = Adresse(adresse["numero"], adresse["type_voie"], adresse["nom_voie"], adresse["code_postal"], adresse["ville"], adresse["pays"], 0, 0)

        ma_commande = Commande(commande["_id"], commande["date_commande"], commande["etat"], commande["prix_total"], commande["frais_livraison"], commande["id_utilisateur"])
        ma_commande.adresse = mon_adresse
        lignes = []
        cpt = 0
        for ligne in commande["produit_commande"]:
            cpt += 1
            ma_ligne = ProduitCommande(cpt, ligne["quantite"], ligne["prix"], ligne["id_produit"], ligne["nom"], ligne["desc"], ligne["spec_tech"], ligne["couleur"], ligne["image"])
            lignes.append(ma_ligne)
        ma_commande.liste_produit_commande = lignes
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

    collection.update_one({"_id": ObjectId(id_commande)}, {"$set": {"etat": etat}})

