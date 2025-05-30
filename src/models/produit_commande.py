class ProduitCommande:

    def __init__(
        self, id: int, quantite: int, prix: float, id_produit: int, nom: str, desc: str, spec_tech: str, couleur: str, image: str
    ) -> None:
        """Instanciation d'une ligne de commande ProduitCommande

        Args:
            id (int): identifiant du ProduitCommande (pk)
            quantite (int): quantite commandee
            prix (float): prix unitaire du produit lors de la commande
            id_produit (int): identifiant du produit commande (fk)
            nom (str): nom du produit
            desc (str): description du produit
            spec_tech (str): specifications techniques du prooduit
            couleur (str): couleur du produit
            image (str): URI de l'image du produit
        """
        self.id = id
        self.quantite = quantite
        self.prix = prix
        self.id_produit = id_produit
        self.nom = nom 
        self.desc = desc
        self.spec_tech = spec_tech
        self.couleur = couleur
        self.image = image
