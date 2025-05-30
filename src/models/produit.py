from bson import ObjectId

class Produit:
    def __init__(
        self,
        id: ObjectId,
        nom: str,
        description: str,
        spec_tech: str,
        couleur: str,
        image: str,
        prix: float,
        stock: int,
        ventes: int,
        actif: int
    ) -> None:
        """Instanciation d'un Produit

        Args:
            id (ObjectId): identifiant du produit
            nom (str): Nom du produit
            description (str): Description du produit
            spec_tech (str): Specifications technioques du produit
            couleur (str): Couleur
            image (str): URI de l'image du produit
            prix (float): prix unitaire du produit
            stock (int): Stock disponible du produit
            ventes (int): Nombre de ventes totales du produit
            actif (int): Produit actif à la vente
        """
        self.id = id
        self.nom = nom
        self.description = description
        self.spec_tech = spec_tech
        self.couleur = couleur
        self.image = image
        self.prix = prix
        self.stock = stock
        self.ventes = ventes
        self.actif = actif

# Fonction pour afficher l'image de stock
def afficher_image_stock(stock):
    """
    Affiche une image et un message en fonction du niveau de stock.

    Args:
        stock (int): Niveau de stock du produit.

    Returns:
        str: Message et emoji indiquant le niveau de stock.
    """
    
    if stock >= 3:
        return f"🟢  En stock : {stock} disponibles"
    elif stock == 0:
        return f"🔴  Produit victime de son succès"
    else:
        return f"🟠   Bientôt en rupture de stock"