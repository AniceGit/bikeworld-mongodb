import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from src.controllers.produit_controller import get_produits
from src.controllers.commande_controller import get_commandes
from pages.sidebar import afficher_sidebar
from src.tools.session import init_session
import pymongo

# Connexion à MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["bikeworld-mongo"]
collection = db["commande"]

# Initialisation de la session
init_session()

# Redirection si l'utilisateur n'est pas connecté ou n'est pas admin
if not st.session_state.get("utilisateur"):
    st.switch_page("pages/connexion.py")

if not st.session_state['utilisateur'].is_admin():
    st.switch_page("accueil.py")

# Affichage de la sidebar
afficher_sidebar()

def afficher_graph_ventes():
    st.title("Graphique des Ventes par Produit")

    # Widgets pour sélectionner la période
    start_date = st.date_input("Date de début", datetime(2025, 1, 1))
    end_date = st.date_input("Date de fin", datetime(2025, 12, 31))

    # Récupération des commandes depuis MongoDB
    commandes = list(collection.find({}))

    if not commandes:
        st.write("Aucune commande trouvée !")
        return

    # Extraction des noms de produits uniques pour le filtre
    noms_produits = set()
    for commande in commandes:
        for produit in commande.get("produit_commande", []):
            noms_produits.add(produit["nom"])
    noms_produits = list(noms_produits)

    # Widget pour sélectionner un produit
    produit_selectionne = st.selectbox("Sélectionnez un produit", ["Tous"] + noms_produits)

    data = []

    # Transformation des données pour le graphique
    for commande in commandes:
        try:
            commande_date = datetime.strptime(commande["date_commande"], "%Y-%m-%d").date()
            if start_date <= commande_date <= end_date:
                for produit in commande["produit_commande"]:
                    if produit_selectionne == "Tous" or produit["nom"] == produit_selectionne:
                        data.append({
                            "ID": commande["_id"],
                            "Nom": produit["nom"],
                            "Ventes": produit["quantite"],
                            "Date": commande["date_commande"]
                        })
        except KeyError as e:
            st.error(f"Clé manquante dans les données de commande: {e}")
            continue

    if not data:
        st.write("Aucune vente trouvée pour la période sélectionnée !")
        return

    df = pd.DataFrame(data)

    # Agrégation des ventes par produit
    df_aggregated = df.groupby('Nom')['Ventes'].sum().reset_index()

    # Création du graphique avec Plotly
    fig = px.bar(df_aggregated, x="Nom", y="Ventes", title=f"Ventes par Produit du {start_date} au {end_date}")
    st.plotly_chart(fig)

afficher_graph_ventes()