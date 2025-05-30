import time
import streamlit as st
import pandas as pd
from src.models.adresse import Adresse
from controllers.produit_controller import get_produit_nom_by_id
from controllers.utilisateur_controller import get_utilisateur_by_id
from pages.sidebar import afficher_sidebar
from src.tools.session import init_session
from src.controllers.commande_controller import get_commandes, modifier_etat_commande, supprimer_commande

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

st.title("Bienvenue sur la page d'administration des commandes !")

# Récupération de toutes les commandes de tous les utilisateurs
commandes = get_commandes()

if not commandes:
    st.write("Aucune commande !")
else:

    data = []

    # Création du dataframe pandas
    for cmd in commandes:

        utilisateur = get_utilisateur_by_id(cmd.id_utilisateur)
        data.append(
            {
                "ID": cmd.id,
                "Client": f"{utilisateur.prenom} {utilisateur.nom}",
                "Date": cmd.date_commande,
                "Frais de livraison (€)": f"{cmd.frais_livraison:.2f}",
                "Total (€)": f"{cmd.prix_total:.2f}",
                "Etat": cmd.etat,
            }
        )

    df = pd.DataFrame(data)

    # Création du dataframe streamlit pour le formattage
    st.dataframe(
        df,
        column_config={
            "Frais de livraison (€)": st.column_config.NumberColumn(format="euro"),
            "Total (€)": st.column_config.NumberColumn(format="euro"),
        },
        hide_index=True,
    )


    #Graphique seaborn des ventes par produit
    ventes_par_produit=[]
    for ligne in cmd.liste_produit_commande:
        produit_nom = get_produit_nom_by_id(ligne.id_produit)
        quantite = ligne.quantite
        if produit_nom in ventes_par_produit:
            ventes_par_produit[produit_nom] += quantite
        else:
            ventes_par_produit[produit_nom] = quantite

    # Création du DataFrame pour seaborn
    df_ventes = pd.DataFrame(list(ventes_par_produit.items()), columns=['Produit', 'Quantité'])

    # Création du graphique avec seaborn
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Produit', y='Quantité', data=df_ventes)
    plt.xlabel("Produit")
    plt.ylabel("Quantité vendue")
    plt.title("Ventes par produit")
    plt.xticks(rotation=45)

    st.pyplot(plt)


    # Selection de la commande à "gérer" dans la partie basse
    commande_ids = [cmd.id for cmd in commandes]
    selected_id = st.selectbox("Sélectionner une commande :", commande_ids)

    if selected_id:
        cmd = next((c for c in commandes if c.id == selected_id), None)
        if cmd:
            st.subheader(f"🧾 Détails de la commande {cmd.id}")
            st.write(f"Date : {cmd.date_commande}")
            adresse: Adresse = cmd.adresse
            st.write(
                f"Adresse : {adresse.numero} {adresse.type_voie} {adresse.nom_voie}, {adresse.code_postal} {adresse.ville}"
            )

            # Création du dataframe pandas
            ligne_df = pd.DataFrame(
                [
                    {
                        "Produit": get_produit_nom_by_id(l.id_produit),
                        "Quantité": l.quantite,
                        "Prix unitaire (€)": f"{l.prix:.2f}",
                        "Total (€)": f"{l.quantite * l.prix :.2f}",
                    }
                    for l in cmd.liste_produit_commande
                ]
            )

            # Création du dataframe streamlit pour formattage
            st.dataframe(
                ligne_df,
                column_config={
                    "Prix unitaire (€)": st.column_config.NumberColumn(format="euro"),
                    "Total (€)": st.column_config.NumberColumn(format="euro"),
                },
                hide_index=True,
            )

            # Actions disponibles si l'état de la commande est "Validée"
            if cmd.etat == "Validee":
                colonnes = st.columns(2)
                with colonnes[0]:
                    if st.button(f"🗑️ Supprimer la commande {cmd.id}", key=f"supprimer_{cmd.id}"):
                        supprimer_commande(cmd.id)
                        with st.spinner(text="Veuillez patienter", show_time=False):
                            st.success(f"Commande {cmd.id} supprimée.")
                            time.sleep(2)
                        st.switch_page("pages/admin_commandes.py")
                
                with colonnes[1]:
                    if st.button(f"📑 Passer en préparation {cmd.id}", key=f"preparer_{cmd.id}"):
                        modifier_etat_commande(cmd.id, "En preparation")
                        with st.spinner(text="Veuillez patienter", show_time=False):
                            st.success(f"Commande {cmd.id} en cours de préparation.")
                            time.sleep(.2)
                        st.switch_page("pages/admin_commandes.py")

            # Actions disponibles si l'état de la commande est "En préparation"
            if cmd.etat == "En preparation":
                if st.button(f"📦 Expédier la commande {cmd.id}", key=f"expedier{cmd.id}"):
                    modifier_etat_commande(cmd.id, "Expediee")
                    with st.spinner(text="Veuillez patienter", show_time=False):
                        st.success(f"Commande {cmd.id} expédiée.")
                        time.sleep(.2)
                    st.switch_page("pages/admin_commandes.py")
