import streamlit as st
import pandas as pd
import time
from src.tools.session import init_session
from pages.sidebar import afficher_sidebar
from src.controllers.commande_controller import (
    supprimer_commande,
    get_commandes_by_utilisateur,
    get_adresse_commande,
)
from src.controllers.produit_controller import get_produit_nom_by_id

# Initialisation de la session
init_session()

# si l'utilisateur n'est pas connecté, il est redirigé vers la page de connexion
if not st.session_state["utilisateur"]:
    st.switch_page("pages/connexion.py")

# Affichage de la sidebar
afficher_sidebar()
st.title("Vos commandes")

# Récupération des commandes du client
commandes = get_commandes_by_utilisateur(st.session_state["utilisateur"].id)

if not commandes:
    st.write("Vous n'avez passé aucune commande !")
else:

    data = []

    # Création du dataframe pandas
    for cmd in commandes:

        data.append(
            {
                "ID": cmd.id,
                "Date": cmd.date_commande,
                "Frais de livraison (€)": f"{cmd.frais_livraison:.2f}",
                "Total (€)": f"{cmd.prix_total:.2f}",
                "Etat": cmd.etat,
            }
        )

    df = pd.DataFrame(data)

    # Création du dataframe streamlit
    st.dataframe(
        df,
        column_config={
            "Frais de livraison (€)": st.column_config.NumberColumn(format="euro"),
            "Total (€)": st.column_config.NumberColumn(format="euro"),
        },
        hide_index=True,
    )

    # Sélection de la commande dans la liste
    commande_ids = [cmd.id for cmd in commandes]
    selected_id = st.selectbox("Sélectionner une commande :", commande_ids)

    if selected_id:
        cmd = next((com for com in commandes if com.id == selected_id), None)
        if cmd:
            st.subheader(f"🧾 Détails de la commande {cmd.id}")
            st.write(f"Date : {cmd.date_commande}")
            adresse = get_adresse_commande(cmd.id_adresse)
            st.write(
                f"Adresse : {adresse.numero} {adresse.type_voie} {adresse.nom_voie}, {adresse.code_postal} {adresse.ville}"
            )

            # Création du dataframe pandas pour les lignes de commande
            ligne_df = pd.DataFrame(
                [
                    {
                        "Produit": get_produit_nom_by_id(lig.id_produit),
                        "Quantité": lig.quantite,
                        "Prix unitaire (€)": f"{lig.prix:.2f}",
                        "Total (€)": f"{lig.quantite * lig.prix :.2f}",
                    }
                    for lig in cmd.liste_produit_commande
                ]
            )

            # Création du dataframe streamlit
            st.dataframe(
                ligne_df,
                column_config={
                    "Prix unitaire (€)": st.column_config.NumberColumn(format="euro"),
                    "Total (€)": st.column_config.NumberColumn(format="euro"),
                },
                hide_index=True,
            )

            # Action de suppression de commande si état = "Validée"
            if cmd.etat == "Validee":
                if st.button(f"🗑️ Supprimer la commande {cmd.id}", key=f"delete_{cmd.id}"):
                    supprimer_commande(cmd.id)
                    with st.spinner(text="Veuillez patienter", show_time=False):
                        st.success(f"Commande {cmd.id} supprimée.")
                        time.sleep(2)
                    st.switch_page("pages/commandes.py")
