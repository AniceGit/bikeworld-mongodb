class ProduitCommande:

    def __init__(
        self, id: int, quantite: int, prix: float, id_produit: int, id_commande: int
    ) -> None:
        """Instanciation d'une ligne de commande ProduitCommande

        Args:
            id (int): identifiant du ProduitCommande (pk)
            quantite (int): quantite commandee
            prix (float): prix unitaire du produit lors de la commande
            id_produit (int): identifiant du produit commande (fk)
            id_commande (int): identifiant de la commande (fk)
        """
        self.id = id
        self.quantite = quantite
        self.prix = prix
        self.id_produit = id_produit
        self.id_commande = id_commande
