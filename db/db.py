import sqlite3
import os
import json


def init_db(data) -> None:
    """Réinitialisation de la base de données

    Args:
        data (dict): dictionnaire contenant les données du fichier JSON

    """
    with sqlite3.connect("bikeworld.db") as conn:

        cur = conn.cursor()

        # destruction de la table des utilisateurs existante
        print("Creation de la table utilisateur")
        cur.execute(
            """
            DROP TABLE IF EXISTS utilisateur
        """
        )

        # creation de la table des utilisateurs
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS utilisateur (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                prenom TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                telephone TEXT NOT NULL
            )
        """
        )

        # destruction de la table des adresses existante
        print("Creation de la table adresse")
        cur.execute(
            """
            DROP TABLE IF EXISTS adresse
        """
        )

        # creation de la table des adresses
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS adresse (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero TEXT NOT NULL,
                type_voie TEXT NOT NULL,
                nom_voie TEXT NOT NULL,
                code_postal TEXT NOT NULL,
                ville TEXT NOT NULL,
                pays TEXT NOT NULL,
                defaut INTEGER NOT NULL,
                active INTEGER NOT NULL,
                id_utilisateur INTEGER NOT NULL,
                FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id)
            )
        """
        )

        # destruction de la table des produits existante
        print("Creation de la table produit")
        cur.execute(
            """
            DROP TABLE IF EXISTS produit
        """
        )

        # creation de la table des produits
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS produit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                desc TEXT NOT NULL,
                spec_tech TEXT NOT NULL,
                couleur TEXT NOT NULL,
                image TEXT NOT NULL,
                prix REAL NOT NULL,
                stock INTEGER NOT NULL,
                ventes INTEGER NOT NULL,
                actif INTEGER NOT NULL
            )
        """
        )

        # destruction de la table des commandes existante
        print("Creation de la table commande")
        cur.execute(
            """
            DROP TABLE IF EXISTS commande
        """
        )

        # creation de la table des commandes
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS commande (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date_commande TEXT NOT NULL,
                etat TEXT NOT NULL,
                prix_total REAL NOT NULL,
                frais_livraison REAL NOT NULL,
                id_utilisateur INTEGER NOT NULL,
                id_adresse INTEGER NOT NULL,
                FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id)
                FOREIGN KEY (id_adresse) REFERENCES adresse(id)
            )
        """
        )

        # destruction de la table des lignes (produit_commande) existante
        print("Creation de la table produit_commande")
        cur.execute(
            """
            DROP TABLE IF EXISTS produit_commande
        """
        )

        # creation de la table des commandes
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS produit_commande (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quantite INT NOT NULL,
                prix REAL NOT NULL,
                id_produit INTEGER NOT NULL,
                id_commande INTEGER NOT NULL,
                FOREIGN KEY (id_produit) REFERENCES produit(id)
                FOREIGN KEY (id_commande) REFERENCES commande(id)
            )
        """
        )

        # destruction de la table des roles existante
        print("Creation de la table roles")
        cur.execute(
            """
            DROP TABLE IF EXISTS roles
        """
        )

        # creation de la table des roles
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL
            )
        """
        )

        # destruction de la table des roles_utilisateur existante
        print("Creation de la table roles_utilisateur")
        cur.execute(
            """
            DROP TABLE IF EXISTS roles_utilisateur
        """
        )

        # creation de la table des roles_utilisateur
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS roles_utilisateur (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_utilisateur INTEGER NOT NULL,
                id_role INTEGER NOT NULL,
                FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id)
                FOREIGN KEY (id_role) REFERENCES role(id)
            )
        """
        )


        print(f"Population de la table utilisateur")
        # Boucle pour insert les utilisateurs du fichier data.json
        utilisateurs = data.get("utilisateur")

        cur.executemany(
            """
            INSERT INTO utilisateur (nom, prenom, email, password, telephone)
                VALUES (:nom, :prenom, :email, :password, :telephone)
            """,
            utilisateurs,
        )

        print(f"Population de la table adresse")
        # Boucle pour insert les adresses du fichier data.json
        adresses = data.get("adresse")

        cur.executemany(
            """
            INSERT INTO adresse (numero, type_voie, nom_voie, code_postal, ville, pays, defaut, active, id_utilisateur)
                VALUES (:numero, :type_voie, :nom_voie, :code_postal, :ville, :pays, :defaut, :active, :id_utilisateur)
            """,
            adresses,
        )

        print(f"Population de la table produit")
        # Boucle pour insert les produits du fichier data.json
        produits = data.get("produit")

        cur.executemany(
            """
            INSERT INTO produit (nom, desc, spec_tech, couleur, image, prix, stock, ventes, actif)
                VALUES (:nom, :desc, :spec_tech, :couleur, :image, :prix, :stock, :ventes, :actif)
            """,
            produits,
        )

        print(f"Population de la table commande")
        # Boucle pour insert les commandes du fichier data.json
        commandes = data.get("commande")

        cur.executemany(
            """
            INSERT INTO commande (date_commande, etat, prix_total, frais_livraison, id_utilisateur, id_adresse)
                VALUES (:date_commande, :etat, :prix_total, :frais_livraison, :id_utilisateur, :id_adresse)
            """,
            commandes,
        )

        print(f"Population de la table produit_commande")
        # Boucle pour insert les produit_commande du fichier data.json
        produit_commandes = data.get("produit_commande")

        cur.executemany(
            """
            INSERT INTO produit_commande (quantite, prix, id_produit, id_commande)
                VALUES (:quantite, :prix, :id_produit, :id_commande)
            """,
            produit_commandes,
        )

        print(f"Population de la table roles")
        # Boucle pour insert les roles du fichier data.json
        roles = data.get("roles")

        cur.executemany(
            """
            INSERT INTO roles (nom)
                VALUES (:nom)
            """,
            roles,
        )

        print(f"Population de la table roles_utilisateur")
        # Boucle pour insert les roles_utilisateur du fichier data.json
        roles_utilisateur = data.get("roles_utilisateur")

        cur.executemany(
            """
            INSERT INTO roles_utilisateur (id_utilisateur, id_role)
                VALUES (:id_utilisateur, :id_role)
            """,
            roles_utilisateur,
        )

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
