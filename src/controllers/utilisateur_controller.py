import streamlit as st
import json, os
from pymongo import MongoClient
from models.utilisateur import Utilisateur
from models.adresse import Adresse, adresse_from_dict
from bson import ObjectId

# ----création d'un nouvel utilisateur via une inscription----#
def inscrire_utilisateur(
    nom: str, prenom: str, email: str, password: str, telephone: str
) -> bool:
    """
    Inscrit un nouvel utilisateur si l'email n'existe pas déjà dans la base.

    Args:
        nom (str): Nom de l'utilisateur.
        prenom (str): Prénom de l'utilisateur.
        email (str): Email unique de l'utilisateur.
        password (str): Mot de passe de l'utilisateur.
        telephone (str): Numéro de téléphone de l'utilisateur.

    Returns:
        bool: True si l'inscription a réussi, False si l'email est déjà utilisé.

    Effets de bord:
        Affiche un message d'erreur ou de succès via Streamlit.
    """
    utilisateur = get_utilisateur_by_email(email)
    if utilisateur:
        st.error("Cet email est déjà utilisé.")
        return False
    else:
        creer_utilisateur(nom, prenom, email, password, telephone)
        st.success("Inscription réussie. Vous pouvez maintenant vous connecter.")
        return True


def creer_utilisateur(
    nom: str, prenom: str, email: str, password: str, telephone: str
) -> None:
    """
    Insère un nouvel utilisateur dans la base MongoDB.

    Args:
        nom (str): Nom de l'utilisateur.
        prenom (str): Prénom de l'utilisateur.
        email (str): Email de l'utilisateur.
        password (str): Mot de passe de l'utilisateur.
        telephone (str): Numéro de téléphone de l'utilisateur.

    Returns:
        None

    Effets de bord:
        Insère un nouvel utilisateur dans la collection `utilisateur`.
    """
    client = MongoClient("mongodb://localhost:27017/")
    db = client["bikeworld-mongo"]
    collection = db["utilisateur"]

    utilisateur = Utilisateur(id=0, nom=nom, prenom=prenom, email=email, password=password, telephone=telephone)

    utilisateur_to_insert = {
        "nom": utilisateur.nom,
        "prenom": utilisateur.prenom,
        "email": utilisateur.email,
        "password": utilisateur.password,
        "telephone": utilisateur.telephone,
        "roles":utilisateur.roles,
        "adresse":utilisateur.adresses
    }

    result = collection.insert_one(utilisateur_to_insert)


# ----connexion d'un utilisateur avec utilisation d'un get-email pour vérifier si cet utilisateur existe et s'il a ce password----#
def connecter_utilisateur(email: str, password: str) -> bool:
    """
    Authentifie un utilisateur via son email et son mot de passe.

    Args:
        email (str): Email de l'utilisateur.
        password (str): Mot de passe de l'utilisateur.

    Returns:
        bool: True si la connexion est réussie, False sinon.

    Effets de bord:
        Enregistre l'utilisateur dans la session Streamlit en cas de succès.
        Affiche un message d'erreur ou de succès via Streamlit.
        Sauvegarde l'utilisateur dans un fichier JSON.
    """
    utilisateur: Utilisateur = get_utilisateur_by_email(email)
    if utilisateur and utilisateur.password == password:
        st.session_state["utilisateur"] = utilisateur
        st.success(f"Bienvenue, {utilisateur.prenom} !")
        sauvegarder_json_utilisateur(utilisateur)
        return True
    else:
        st.error("Identifiants incorrects.")
        return False


def get_utilisateur_by_email(email: str) -> Utilisateur | None:
    """
    Récupère un utilisateur à partir de son email depuis la base de données.

    Args:
        email (str): Email de l'utilisateur recherché.

    Returns:
        Utilisateur | None: Instance Utilisateur si trouvé, sinon None.
    """
    client = MongoClient("mongodb://localhost:27017/")
    db = client["bikeworld-mongo"]
    collection = db["utilisateur"]

    result:dict = collection.find_one({"email" :  email})
    if result:
        utilisateur = Utilisateur(
            id = result.get("_id"),
            nom = result.get("nom"),
            prenom = result.get("prenom"),
            email = result.get("email"),
            password = result.get('password'),
            telephone = result.get("telephone"),
            roles = result.get("roles"),
            adresses = [adresse_from_dict(a) for a in result.get("adresse")]
        )
        return utilisateur
    else :
        return None

def get_adresse_utilisateur_defaut(utilisateur:Utilisateur) -> Adresse | None:
    """
    Récupère l'adresse par défaut dans la liste d'adresses dans l'utilisateur

    Args:
        utilisateur (Utilisateur): utilisateur

    Returns:
        Adresse | None: Instance Adresse si trouvé, sinon None.
    """
    adresse_defaut:Adresse = None
    for adresse in utilisateur.adresses:
        if adresse.defaut == 1:
            adresse_defaut = adresse
            return adresse_defaut
    return None
    

# # -----Récupérer les adresses d'un utilisateur-----#
# def get_adresses_utilisateur(id: int) -> list[Adresse]:
#     """
#     Récupère toutes les adresses actives associées à un utilisateur donné.

#     Args:
#         id (int): Identifiant de l'utilisateur.

#     Returns:
#         list[Adresse]: Liste d'objets Adresse.

#     Raises:
#         Exception: Si aucune adresse n'est trouvée.
#     """
#     with sqlite3.connect("bikeworld.db") as conn:
#         cur = conn.cursor()
#         cur.execute("SELECT * FROM adresse WHERE id_utilisateur = :id and active = :active", {"id": id, "active": 1})
#         result_adresses = cur.fetchall()
#         if result_adresses is None:
#             raise Exception(f"Aucune adresse")

#         adresses = []
#         for (
#             id,
#             numero,
#             type_voie,
#             nom_voie,
#             code_postal,
#             ville,
#             pays,
#             defaut,
#             active,
#             id_utilisateur,
#         ) in result_adresses:
#             adresses.append(
#                 Adresse(
#                     id,
#                     numero,
#                     type_voie,
#                     nom_voie,
#                     code_postal,
#                     ville,
#                     pays,
#                     defaut,
#                     active,
#                     id_utilisateur,
#                 )
#             )
#         return adresses

# # -----Créer adresse-----#
# def creer_adresse(
#     numero: str,
#     type_voie: str,
#     nom_voie: str,
#     code_postal: str,
#     ville: str,
#     pays: str,
#     defaut: int,
#     active: int,
#     id_utilisateur: int,
# ) -> bool:
#     """
#     Insère une nouvelle adresse dans la base de données.

#     Args:
#         numero (str): Numéro de rue.
#         type_voie (str): Type de voie (rue, avenue...).
#         nom_voie (str): Nom de la voie.
#         code_postal (str): Code postal.
#         ville (str): Ville.
#         pays (str): Pays.
#         defaut (int): Indicateur si adresse par défaut (1 = oui, 0 = non).
#         active (int): Indicateur si adresse active (1 = oui, 0 = non).
#         id_utilisateur (int): Identifiant de l'utilisateur propriétaire.

#     Returns:
#         bool: True si l'insertion a réussi.

#     Effets de bord:
#         Affiche un message de succès via Streamlit.
#     """
#     with sqlite3.connect("bikeworld.db") as conn:
#         cur = conn.cursor()
#         cur.execute(
#             """
#             INSERT INTO adresse (numero, type_voie, nom_voie, code_postal, ville, pays, defaut, active, id_utilisateur)
#             VALUES (:numero, :type_voie, :nom_voie, :code_postal, :ville, :pays, :defaut, :active, :id_utilisateur)
#         """,
#             {
#                 "numero": numero,
#                 "type_voie": type_voie,
#                 "nom_voie": nom_voie,
#                 "code_postal": code_postal,
#                 "ville": ville,
#                 "pays": pays,
#                 "defaut": defaut,
#                 "active": active,
#                 "id_utilisateur": id_utilisateur,
#             },
#         )
#         st.success("Nouvelle adresse créée avec succès !")
#         return True


# # -----Modifier adresse-----#
# def modifier_adresse_utilisateur(nouvelle_adresse: Adresse) -> None:
#     """
#     Met à jour une adresse existante dans la base de données.

#     Args:
#         nouvelle_adresse (Adresse): Objet Adresse contenant les nouvelles données.

#     Returns:
#         None

#     Effets de bord:
#         Met à jour la ligne correspondante dans la table `adresse`.
#     """
#     with sqlite3.connect("bikeworld.db") as conn:
#         cur = conn.cursor()
#         cur.execute(
#             """UPDATE adresse SET numero = :numero, type_voie = :type_voie, nom_voie = :nom_voie, code_postal = :code_postal, ville = :ville, pays = :pays, defaut = :defaut, active = :active WHERE id = :id_adresse
#                     """,
#             {
#                 "numero": nouvelle_adresse.numero,
#                 "type_voie": nouvelle_adresse.type_voie,
#                 "nom_voie": nouvelle_adresse.nom_voie,
#                 "code_postal": nouvelle_adresse.code_postal,
#                 "ville": nouvelle_adresse.ville,
#                 "pays": nouvelle_adresse.pays,
#                 "defaut": nouvelle_adresse.defaut,
#                 "active": nouvelle_adresse.active,
#                 "id_adresse": nouvelle_adresse.id,
#             },
#         )

# # -----Supprimer adresse-----#
# def supprimer_adresse_utilisateur(id_adresse:int, utilisateur:Utilisateur) -> bool:
#     """
#     Désactive une adresse (active = 0, defaut = 0) dans la base de données.

#     Args:
#         id_adresse (int): Identifiant de l'adresse à désactiver.
#         utilisateur (Utilisateur): Utilisateur propriétaire de l'adresse.

#     Returns:
#         bool: True si la suppression (désactivation) a réussi.

#     Effets de bord:
#         Met à jour la base.
#         Sauvegarde la session utilisateur dans un fichier JSON.
#         Affiche un message de succès via Streamlit.
#     """
#     with sqlite3.connect("bikeworld.db") as conn:
#         cur = conn.cursor()
#         cur.execute(
#             """UPDATE adresse SET defaut = :defaut, active = :active WHERE id = :id_adresse
#                     """,
#             {
#                 "defaut":0,
#                 "active":0,
#                 "id_adresse": id_adresse,
#             },
#         )
#         st.success("Adresse supprimée avec succès !")
#         return True


# -----modification de l'utilisateur-----#
def modifier_utilisateur(nouvel_utilisateur: Utilisateur) -> bool:
    """
    Met à jour les informations d'un utilisateur dans la base de données.

    Args:
        nouvel_utilisateur (Utilisateur): Objet Utilisateur avec les nouvelles données.

    Returns:
        bool: True si la modification a réussi.

    Effets de bord:
        Met à jour la ligne correspondante dans la table `utilisateur`.
        Sauvegarde la session utilisateur dans un fichier JSON.
        Affiche un message de succès via Streamlit.
    """
    client = MongoClient("mongodb://localhost:27017/")
    db = client["bikeworld-mongo"]
    collection = db["utilisateur"]

    result = collection.update_one(
            {"_id": nouvel_utilisateur.id},
            {
                "$set":{
                    "nom":nouvel_utilisateur.nom,
                    "prenom":nouvel_utilisateur.prenom,
                    "email":nouvel_utilisateur.email,
                    "telephone":nouvel_utilisateur.telephone,
                    "adresse":[a.to_dict() for a in nouvel_utilisateur.adresses]
                }
            })
    if result.matched_count == 0:
        st.warning("Aucun utilisateur trouvé avec cet ID.")
        return False
    if result.modified_count == 0:
        st.warning("Aucune modification effectuée.")
        return False
    
    sauvegarder_json_utilisateur(nouvel_utilisateur)
    st.success("Utilisateur modifié avec succès !")
    return True

# -----déconnexion de l'utilisateur-----#
def deconnecter_utilisateur() -> str:
    """
    Déconnecte l'utilisateur courant de la session Streamlit.

    Returns:
        str: Prénom de l'utilisateur déconnecté.

    Effets de bord:
        Supprime la session utilisateur en mémoire et supprime le fichier JSON de session s'il existe.
    """
    if (
        "utilisateur" in st.session_state
        and st.session_state["utilisateur"] is not None
    ):
        prenom = st.session_state["utilisateur"].prenom
        st.session_state["utilisateur"] = None
        if os.path.exists("db/utilisateur_session.json"):
            supprimer_json_utilisateur()
    return prenom


# -----sauvegarde de l'utilisateur connecté dans un json-----#
def sauvegarder_json_utilisateur(utilisateur: Utilisateur) -> None:
    """
    Sauvegarde les données de l'utilisateur connecté dans un fichier JSON.

    Args:
        utilisateur (Utilisateur): Utilisateur à sauvegarder.

    Returns:
        None

    Effets de bord:
        Crée ou écrase le fichier 'db/utilisateur_session.json'.
        Affiche un message d'erreur via Streamlit en cas de problème d'écriture.
    """
    try:
        with open("db/utilisateur_session.json", "w") as f:
            json.dump(utilisateur.to_dict(), f)
    except Exception as e:
        st.error("Erreur de sauvegarde de session : " + str(e))


# -----supprimer le json utilisateur qui sert à session-----#
def supprimer_json_utilisateur() -> None:
    """
    Supprime le fichier JSON contenant la session utilisateur.

    Returns:
        None

    Effets de bord:
        Supprime le fichier 'db/utilisateur_session.json' s'il existe.
    """
    os.remove("db/utilisateur_session.json")



def get_utilisateur_by_id(id_utilisateur: int) -> Utilisateur | None:
    """
    Récupère un utilisateur dans la base de données à partir de son id.

    Paramètres:
    id_utilisateur (int): Identifiant de l'utilisateur à rechercher.

    Retourne:
    tuple: Un tuple contenant les informations de l'utilisateur si l'email est trouvé,
           ou None si aucun utilisateur n'est trouvé avec cet email.
    """
    client = MongoClient("mongodb://localhost:27017/")
    db = client["bikeworld-mongo"]
    collection = db["utilisateur"]
    print (id_utilisateur)
    result:dict = collection.find_one({"_id" :  ObjectId(id_utilisateur)})


    utilisateur = Utilisateur(
        id = result.get("_id"),
        nom = result.get("nom"),
        prenom = result.get("prenom"),
        email = result.get("email"),
        password = result.get("password"),
        telephone = result.get("telephone"),
        roles = result.get("roles"),
        adresses = result.get("adresse")
    )

    if utilisateur:
        return utilisateur
    else :
        return None
