import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from controllers.produit_controller import get_produits
from pages.sidebar import afficher_sidebar
from src.tools.session import init_session

# Initialisation de la session
init_session()

# si l'utilisateur n'est pas connecté, il est redirigé vers la page de connexion
if not st.session_state["utilisateur"]:
    st.switch_page("pages/connexion.py")

# si l'utilisateur n'est pas "admin", il est redirigé vers la page d'accueil
if not st.session_state['utilisateur'].is_admin():
    st.switch_page("accueil.py")

# affichage de la sidebar
afficher_sidebar()

def afficher_graph_produits():
    st.title("Graphique des Ventes par Produit")

    # Widgets pour sélectionner la période
    start_date = st.date_input(
        "Date de début",
        datetime.now() - pd.DateOffset(days=30))  # Par défaut, 30 jours avant aujourd'hui

    end_date = st.date_input(
        "Date de fin",
        datetime.now())  # Par défaut, aujourd'hui

    # Récupération de tous les produits de la base
    produits = get_produits()  # Assurez-vous que cette fonction retourne une liste de produits

    if not produits:
        st.write("Aucun produit trouvé !")
    else:
        data = []

        # Filtrer les produits en fonction de la période sélectionnée
        for produit in produits:
            # Assurez-vous que chaque produit a un attribut 'date' ou similaire
            # Remplacez 'date' par le champ approprié de votre modèle de données
            if hasattr(produit, 'date') and start_date <= produit.date <= end_date:
                data.append(
                    {
                        "ID": produit.id,
                        "Nom": produit.nom,
                        "Ventes": produit.ventes,
                    }
                )

        if not data:
            st.write("Aucun produit trouvé pour la période sélectionnée !")
        else:
            df = pd.DataFrame(data)

            # Création du graphique avec Plotly
            fig = px.bar(df, x="Nom", y="Ventes", title=f"Ventes par Produit du {start_date} au {end_date}")
            st.plotly_chart(fig)

afficher_graph_produits()