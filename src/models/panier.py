class Panier:

    def __init__(
        self, date_panier: str, total_panier: float
    ) -> None:
        """Instanciation d'un Panier

        Args:
            date_panier (str): date de la mise au panier
            total_panier (float): prix total de la commande
            frais_livraison (float): montant des frais de livraison
            liste_produits_quantite (list[dict]): liste des produits et leur quantité dans le panier
        """
        self.date_panier = date_panier
        self.total_panier = total_panier
        self.frais_livraison = 25.0
        self.liste_produits_quantite = []

    def recalculer_total_panier(self):
        total_panier = 0
        for item in self.liste_produits_quantite:
            total_panier += item["quantite"] * item["prix"]
        self.total_panier = total_panier
        return self.total_panier

    def get_frais_livraison(self):
        return 25.0 if self.recalculer_total_panier() < 1500 else 0.0

