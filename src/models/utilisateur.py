from typing import List
from src.models.adresse import Adresse
from src.models.adresse import adresse_from_dict
import sqlite3
from bson import ObjectId

class Utilisateur:

    def __init__(
        self, id: int, nom: str, prenom: str, email: str, password: str, telephone: str, adresses: List[Adresse] = None, roles:dict={'admin':False,'superclient':False,'client':True}
    ) -> None:
        """
        Instancie un objet Utilisateur.

        Args:
            id (int): Identifiant unique de l'utilisateur (clé primaire).
            nom (str): Nom de l'utilisateur.
            prenom (str): Prénom de l'utilisateur.
            email (str): Adresse email de l'utilisateur.
            password (str): Mot de passe de l'utilisateur (haché idéalement).
            telephone (str): Numéro de téléphone de l'utilisateur.

        Attributes:
            adresse (Adresse | None): Adresse par défaut de l'utilisateur, initialisée à None.
            roles (list): Liste des rôles associés à l'utilisateur, récupérés depuis la base de données.
        """
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.password = password
        self.telephone = telephone
        self.adresses: List[Adresse] = adresses if adresses else []
        self.roles: dict = roles 


    def to_dict(self) -> dict:
        """
        Convertit l'objet Utilisateur en dictionnaire, prêt pour la sérialisation.

        Returns:
            dict: Un dictionnaire contenant les attributs de l'utilisateur, y compris son adresse et ses rôles.
        """
        print("CECI EST L'ID  ",self.id)
        return {
            #On converti l'id ObjectId en str afin de pouvoir l'injecter dans un json
            "id": str(self.id),
            "nom": self.nom,
            "prenom": self.prenom,
            "email": self.email,
            "password": self.password,
            "telephone": self.telephone,
            "adresses": [adresse.to_dict() for adresse in self.adresses] if self.adresses else [],
            "roles": self.roles
        }


    def is_admin(self) -> bool:
        """
        Vérifie si l'utilisateur a le rôle 'admin'.

        Returns:
            bool: True si l'utilisateur est administrateur, False sinon.
        """
        return self.roles.get("admin")


    def is_superclient(self) -> bool:
        """
        Vérifie si l'utilisateur a le rôle 'superclient'.

        Returns:
            bool: True si l'utilisateur est superclient, False sinon.
        """
        return True if self.roles.get("superclient") else False


def utilisateur_from_dict(data:dict) -> Utilisateur:
    """
    Crée une instance d'Utilisateur à partir d'un dictionnaire.

    Args:
        data (dict): Dictionnaire contenant les données d'un utilisateur. 
                     Peut contenir une clé "adresse" pour initialiser l'adresse.

    Returns:
        Utilisateur: Instance de la classe Utilisateur initialisée avec les données fournies.
    """
    print("UTILISATEUR  ", data["nom"])
    if data.get("adresse"):
        adresses = [adresse_from_dict(a) for a in data.get("adresse", [])]

    utilisateur = Utilisateur(
        #On récupère l'id d'un dictionnaire (json) et on le converti en ObjectId (type sur mongoDB)
        ObjectId(data["id"]),
        data["nom"],
        data["prenom"],
        data["email"],
        data["password"],
        data["telephone"],
        adresses if data.get("adresse") else [],
        data["roles"]
    )
    return utilisateur


# def get_roles(id_utilisateur) -> list:
#     """
#     Récupère la liste des rôles associés à un utilisateur depuis la base de données SQLite.

#     Args:
#         id_utilisateur (int): Identifiant de l'utilisateur dont on souhaite récupérer les rôles.

#     Returns:
#         list: Liste des noms des rôles associés à l'utilisateur.
#     """
#     roles = []
#     with sqlite3.connect("bikeworld.db") as conn:
#         cur = conn.cursor()

#         # Récupération des roles de l'utilisateur
#         cur.execute("""
#             SELECT id_role
#             FROM roles_utilisateur
#             WHERE id_utilisateur = :id_utilisateur
#         """,
#             {"id_utilisateur": id_utilisateur},
#         )
#         roles_id = cur.fetchall()

#         for id_roles in roles_id:
#             # Récupération des noms des roles
#             cur.execute(
#                 """
#                 SELECT nom
#                 FROM roles
#                 WHERE id = :id
#             """,
#                 {"id": id_roles[0]},
#             )
#             result_roles = cur.fetchall()

#             for nom in result_roles:
#                 roles.append(nom[0])

#     return roles


