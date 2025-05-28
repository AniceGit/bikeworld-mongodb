class Commande:

    def __init__(
        self,
        id: int,
        date_commande: str,
        etat: str,
        prix_total: float,
        frais_livraison: float,
        id_utilisateur: int
    ) -> None:
        """Instanciation d'une Commande

        Args:
            id (int): identifiant de la commande (pk)
            date_commande (str): date de la commande
            etat (str): etat de la commande (Validee, En Preparation, Expediee, Livree)
            prix_total (float): prix total de la commande
            frais_livraison (float): frais de livraison
            id_utilisateur (int): identifiant de l'utilisateur propriétaire de la commande (fk)
            id_adresse (Adresse): adresse de livraison
            liste_produit_commande (list[ProduitCommande]): liste des lignes de la commande
        """
        self.id = id
        self.date_commande = date_commande
        self.etat = etat
        self.prix_total = prix_total
        self.frais_livraison = frais_livraison
        self.id_utilisateur = id_utilisateur
        self.id_adresse = None
        self.liste_produit_commande = None
