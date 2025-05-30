import streamlit as st
from pages.sidebar import afficher_sidebar
from models.utilisateur import Utilisateur
from models.adresse import Adresse
from controllers.utilisateur_controller import (
    modifier_utilisateur,
    sauvegarder_json_utilisateur,
    get_adresse_utilisateur_defaut
)
from tools.session import init_session
import time

init_session()

# Affichage sidebar et titre
afficher_sidebar()

def profil_vue() -> None:
    """
    Affiche et gère la page de profil utilisateur.

    Fonctionnalités :
    - Affiche les informations personnelles (nom, prénom, email, téléphone).
    - Affiche l'adresse par défaut de l'utilisateur.
    - Permet la modification des informations personnelles.
    - Permet de sélectionner, ajouter ou supprimer une adresse liée à l'utilisateur.
    - Synchronise les modifications avec la base de données, la session et un fichier JSON.
    - Empêche la modification si aucune donnée n'a été changée.
    - Utilise des clés dans st.session_state pour gérer l'état des inputs.
    - Navigation entre pages via st.switch_page.

    Étapes clés :
    1. Récupère l'utilisateur connecté depuis la session.
    2. Initialise les champs de formulaire avec les données actuelles.
    3. Récupère les adresses associées à l'utilisateur et les affiche dans un selectbox.
    4. Gère l'état des boutons Modifier et Supprimer selon les données modifiées et la sélection d'adresse.
    5. Met à jour les données utilisateur et adresse par défaut si modification validée.
    6. Permet d'ajouter une nouvelle adresse en naviguant vers la page correspondante.
    7. Permet de supprimer l'adresse sélectionnée et met à jour les données en conséquence.

    Ne retourne rien, affiche directement la page Streamlit.
    """
    st.title("Profil")

    # Récupération des infos de l'utilisateur connecté
    utilisateur: Utilisateur = st.session_state["utilisateur"]
    adresse: Adresse = get_adresse_utilisateur_defaut(utilisateur)

    st.markdown("### 👤 Informations ")

    st.markdown(f"""
     **Nom :** {utilisateur.nom}  
     **Prénom :** {utilisateur.prenom}  
     **Email :** {utilisateur.email}  
     **Téléphone :** {utilisateur.telephone}  
     **Adresse :** {adresse.__str__() if adresse else "Non renseignée"}
    """)

    if "nom_key" not in st.session_state or st.session_state.nom_key == "":
        st.session_state.nom_key = utilisateur.nom
    if "prenom_key" not in st.session_state or st.session_state.prenom_key == "":
        st.session_state.prenom_key = utilisateur.prenom
    if "email_key" not in st.session_state or st.session_state.email_key == "":
        st.session_state.email_key = utilisateur.email
    if "telephone_key" not in st.session_state or st.session_state.telephone_key == "":
        st.session_state.telephone_key = utilisateur.telephone

    # Input
    nom = st.text_input("Nom", key="nom_key")
    prenom = st.text_input("Prénom", key="prenom_key")
    email = st.text_input("Email", key="email_key")
    telephone = st.text_input("Téléphone", key="telephone_key")

    # On récupère toutes les adresses liées à cet utilisateur et on les met dans une liste
    adresses: list[Adresse] = utilisateur.adresses
    option = st.selectbox(
        "Choisissez parmi vos adresses",
        (adresse.__str__() for adresse in adresses if adresse.active),
        index=None,
        placeholder="Choisir...",
    )

    # Button disabled si pas d'adresse choisie et si adresse choisie alors button à None si aucun changement
    button_disabled = option == None
    if option is not None:
        adresse_selectionnee = next(
            (adresse for adresse in adresses if adresse.__str__() == option), None
        )
        if (
            utilisateur.nom == nom
            and utilisateur.prenom == prenom
            and utilisateur.email == email
            and utilisateur.telephone == telephone
            and ((adresse == None and adresse_selectionnee == None) or (adresse and adresse == adresse_selectionnee))
        ):
            button_disabled = True

    # On affecte les valeurs insérées au nouvel utilisateur et on le modifie en db, session et json puis on refresh la page
    if st.button("💾 Modifier", disabled=button_disabled):
        nouvel_utilisateur = utilisateur
        nouvel_utilisateur.nom = nom if nom else utilisateur.nom
        nouvel_utilisateur.prenom = prenom if prenom else utilisateur.prenom
        nouvel_utilisateur.email = email if email else utilisateur.email
        nouvel_utilisateur.telephone = telephone if telephone else utilisateur.telephone

        if adresse.__str__() != adresse_selectionnee.__str__():
            for a in nouvel_utilisateur.adresses:
                if a.__str__() == adresse.__str__():
                    a.defaut = 0
                if a.__str__() == adresse_selectionnee.__str__():
                    a.defaut = 1

        modifier_utilisateur(nouvel_utilisateur)
        st.session_state["utilisateur"] = nouvel_utilisateur
        sauvegarder_json_utilisateur(nouvel_utilisateur)
        with st.spinner(text="Veuillez patienter", show_time=False):
            time.sleep(2)
            st.switch_page("pages/profil.py")

    if st.button("📍 Adresse"):
        st.switch_page("pages/adresse.py")

profil_vue()


