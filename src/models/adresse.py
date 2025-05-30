from bson import ObjectId

class Adresse:
    def __init__(
        self,
        numero: str,
        type_voie: str,
        nom_voie: str,
        code_postal: str,
        ville: str,
        pays: str,
        defaut: int,
        active: int,
    ) -> None:
        """
        Initialise une instance de la classe Adresse.

        Args:
            numero (str): Numéro de la rue.
            type_voie (str): Type de la voie (exemple : "rue", "avenue", "boulevard").
            nom_voie (str): Nom de la voie.
            code_postal (str): Code postal associé à l'adresse.
            ville (str): Ville de l'adresse.
            pays (str): Pays de l'adresse.
            defaut (int): Indicateur si l'adresse est l'adresse par défaut de l'utilisateur (1 = oui, 0 = non).
            active (int): Indicateur si l'adresse est active (1 = oui, 0 = non).

        Returns:
            None
        """
        self.numero = numero
        self.type_voie = type_voie
        self.nom_voie = nom_voie
        self.code_postal = code_postal
        self.ville = ville
        self.pays = pays
        self.defaut = defaut
        self.active = active

    def to_dict(self) -> dict:
        """
        Convertit l'objet Adresse en dictionnaire.

        Returns:
            dict: Un dictionnaire représentant l'adresse avec ses attributs.
        """
        return {
            "numero": self.numero,
            "type_voie": self.type_voie,
            "nom_voie": self.nom_voie,
            "code_postal": self.code_postal,
            "ville": self.ville,
            "pays": self.pays,
            "defaut": self.defaut,
            "active": self.active,
        }

    def __str__(self) -> str:
        """
        Retourne une représentation lisible de l'adresse.

        Returns:
            str: Une chaîne formatée décrivant l'adresse complète.
        """
        adresse_to_str = f"{self.numero} {self.type_voie} {self.nom_voie} - {self.code_postal} {self.ville} - {self.pays}"
        return adresse_to_str


def adresse_from_dict(data: dict) -> Adresse:
    """
    Crée une instance de la classe Adresse à partir d'un dictionnaire.

    Args:
        data (dict): Dictionnaire contenant les données d'une adresse avec les clés attendues.

    Returns:
        Adresse: Une instance de la classe Adresse initialisée avec les données fournies.
    """
    return Adresse(
        numero=data["numero"],
        type_voie=data["type_voie"],
        nom_voie=data["nom_voie"],
        code_postal=data["code_postal"],
        ville=data["ville"],
        pays=data["pays"],
        defaut=data["defaut"],
        active=data["active"],
    )
