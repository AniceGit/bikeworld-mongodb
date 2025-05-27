import time
import streamlit as st
import pandas as pd
from controllers.produit_controller import get_produit_nom_by_id, get_produits, modifier_produit
from controllers.utilisateur_controller import get_utilisateur_by_id
from pages.sidebar import afficher_sidebar
from src.tools.session import init_session
from src.controllers.commande_controller import get_adresse_commande, get_commandes, modifier_etat_commande, supprimer_commande


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

st.title("Bienvenue sur la page d'administration des produits !")

# Récupération de tous les produits de la base
produits = get_produits()


if not produits:
    st.write("Aucun produit !")
else:

    data = []

    # Création du dataframe pandas
    for produit in produits:
        data.append(
            {
                "ID": produit.id,
                "Nom": produit.nom,
                "Description": produit.description,
                "Spécifications techniques": produit.spec_tech,
                "Couleur": produit.couleur,
                "Image": produit.image,
                "Prix (€)": produit.prix,
                "Stock": produit.stock,
                "Ventes": produit.ventes,
                "Actif": produit.actif
            }
        )

    df = pd.DataFrame(data)

    # Création du dataframe streamlit
    st.dataframe(
        df,
        column_config={
            "Prix (€)": st.column_config.NumberColumn(format="euro"),
        },
        hide_index=True,
    )

    # Selection du produit à "gérer" dans la partie basse
    produits_ids = [produit.id for produit in produits]
    selected_id = st.selectbox("Sélectionner un produit :", produits_ids)

    if selected_id:
        # Affichage des champs pour modification du produit sélectionné
        produit = next((p for p in produits if p.id == selected_id), None)
        id = produit.id
        nom = st.text_input(label="Nom", value=produit.nom)
        description = st.text_input(label="Description", value=produit.description)
        spec_tech = st.text_input(label="Specifications techniques", value=produit.spec_tech)
        couleur = st.text_input(label="Couleur", value=produit.couleur)
        image = st.text_input(label="Image", value=produit.image)
        prix = st.number_input(label="Prix", value=produit.prix)
        stock = st.text_input(label="Stock", value=produit.stock)
        actif = st.checkbox(label="Actif", value=produit.actif)


        if st.button("💾 Modifier"):
            actif_n = 1 if actif else 0
            if nom and description and spec_tech and couleur and image and prix and stock:
                modifier_produit(id, nom, description, spec_tech, couleur, image, prix, stock, actif_n)
                with st.spinner(text="Veuillez patienter", show_time=False):
                    time.sleep(2)
                st.switch_page("pages/admin_produits.py")
            else:
                st.write("Veuillez compléter tous les champs")

