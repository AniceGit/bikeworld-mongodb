from src.models.adresse import Adresse
from src.models.adresse import adresse_from_dict


class Utilisateur:

    def __init__(
        self, id: int, nom: str, prenom: str, email: str, password: str, telephone: str
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
        self.adresse: Adresse = None
        self.roles: list = get_roles(self.id)


    def to_dict(self) -> dict:
        """
        Convertit l'objet Utilisateur en dictionnaire, prêt pour la sérialisation.

        Returns:
            dict: Un dictionnaire contenant les attributs de l'utilisateur, y compris son adresse et ses rôles.
        """
        return {
            "id": self.id,
            "nom": self.nom,
            "prenom": self.prenom,
            "email": self.email,
            "password": self.password,
            "telephone": self.telephone,
            "adresse": self.adresse.to_dict() if self.adresse else None,
            "roles": self.roles if self.roles else []
        }


    def is_admin(self) -> bool:
        """
        Vérifie si l'utilisateur a le rôle 'admin'.

        Returns:
            bool: True si l'utilisateur est administrateur, False sinon.
        """
        return True if "admin" in self.roles else False


    def is_superclient(self) -> bool:
        """
        Vérifie si l'utilisateur a le rôle 'superclient'.

        Returns:
            bool: True si l'utilisateur est superclient, False sinon.
        """
        return True if "superclient" in self.roles else False


def utilisateur_from_dict(data) -> Utilisateur:
    """
    Crée une instance d'Utilisateur à partir d'un dictionnaire.

    Args:
        data (dict): Dictionnaire contenant les données d'un utilisateur. 
                     Peut contenir une clé "adresse" pour initialiser l'adresse.

    Returns:
        Utilisateur: Instance de la classe Utilisateur initialisée avec les données fournies.
    """
    utilisateur = Utilisateur(
        data["id"],
        data["nom"],
        data["prenom"],
        data["email"],
        data["password"],
        data["telephone"],
    )
    if data.get("adresse"):
        utilisateur.adresse = adresse_from_dict(data["adresse"])

    utilisateur.roles = get_roles(data["id"])
    return utilisateur


def get_roles(id_utilisateur) -> list:
    """
    Récupère la liste des rôles associés à un utilisateur depuis la base de données SQLite.

    Args:
        id_utilisateur (int): Identifiant de l'utilisateur dont on souhaite récupérer les rôles.

    Returns:
        list: Liste des noms des rôles associés à l'utilisateur.
    """
    roles = []
    with sqlite3.connect("bikeworld.db") as conn:
        cur = conn.cursor()

        # Récupération des roles de l'utilisateur
        cur.execute("""
            SELECT id_role
            FROM roles_utilisateur
            WHERE id_utilisateur = :id_utilisateur
        """,
            {"id_utilisateur": id_utilisateur},
        )
        roles_id = cur.fetchall()

        for id_roles in roles_id:
            # Récupération des noms des roles
            cur.execute(
                """
                SELECT nom
                FROM roles
                WHERE id = :id
            """,
                {"id": id_roles[0]},
            )
            result_roles = cur.fetchall()

            for nom in result_roles:
                roles.append(nom[0])

    return roles


