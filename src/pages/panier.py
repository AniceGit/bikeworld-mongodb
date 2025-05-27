import streamlit as st
import pandas as pd
from pages.sidebar import afficher_sidebar
from src.tools.session import init_session
from src.controllers.commande_controller import transformer_panier
from src.models.panier import Panier
import time, datetime

# Initialisation de la session
init_session()

# Affichage de la sidebar
afficher_sidebar()
st.title("Mon Panier")


panier = st.session_state.panier
# Recalcul du total du panier
panier.total_panier = panier.recalculer_total_panier()

if panier.total_panier == 0.00:
    st.write("Votre panier est vide")
else:
    # Recalcul des frais de livraison
    panier.frais_livraison = panier.get_frais_livraison()
    st.write(f"Date: {panier.date_panier}")

    # Création du dataframe pandas de l'entete du panier
    df_total = pd.DataFrame(
        [
            {
                "Frais de livraison (€)": f"{panier.frais_livraison:.2f}",
                "Total du panier (€)": f"{panier.total_panier + panier.frais_livraison:.2f}",
            }
        ]
    )

    # Création du dataframe pandas des lignes du panier
    df = pd.DataFrame(
        [
            {
                "Produit": produit_quantite["produit"],
                "Quantité": produit_quantite["quantite"],
                "Prix unitaire (€)": f"{produit_quantite['prix']:.2f}",
                "Total (€)": f"{produit_quantite['total']:.2f}",
            }
            for produit_quantite in panier.liste_produits_quantite
        ]
    )

    # Création du dataframe streamlit de l'entete du panier pour formattage
    st.dataframe(
        df,
        column_config={
            "Prix unitaire (€)": st.column_config.NumberColumn(format="euro"),
            "Total (€)": st.column_config.NumberColumn(format="euro"),
        },
        hide_index=True,
    )

    # Création du dataframe streamlit des lignes du panier pour formattage
    st.dataframe(
        df_total,
        column_config={
            "Frais de livraison (€)": st.column_config.NumberColumn(format="euro"),
            "Total du panier (€)": st.column_config.NumberColumn(format="euro"),
        },
        hide_index=True,
    )

    # Sélection d'une ligne du panier pour suppression
    ligne_panier = [produit_quantite["produit"] for produit_quantite in panier.liste_produits_quantite]
    selected_id = st.selectbox("Sélectionner un produit à supprimer :", ligne_panier)

    if selected_id:
        ligne_panier = next((produit_quantite for produit_quantite in panier.liste_produits_quantite if produit_quantite["produit"] == selected_id), None)


    colonnes = st.columns(2)
    with colonnes[0]:
        if st.button("🗑️ Supprimer du panier"):
            liste_panier = panier.liste_produits_quantite
            liste_panier.remove(ligne_panier)

            panier.total_panier = panier.recalculer_total_panier()
            panier.frais_livraison = panier.get_frais_livraison()

            with st.spinner(text="Veuillez patienter", show_time=False):
                time.sleep(2)
            st.switch_page("pages/panier.py")


    # Transformation du panier en commande
    with colonnes[1]:
        if st.button("📑 Passer la commande"):
            if not st.session_state["utilisateur"]:
                st.switch_page("pages/connexion.py")
            else:
                if not transformer_panier():
                    st.error("Veuillez renseigner une adresse par défaut")
                    with st.spinner(text="Veuillez patienter", show_time=False):
                        time.sleep(2)
                    st.switch_page("pages/profil.py")

                st.session_state.panier = Panier(str(datetime.date.today()), 0.0)

                with st.spinner(text="Veuillez patienter", show_time=False):
                    time.sleep(2)
                st.switch_page("pages/commandes.py")
