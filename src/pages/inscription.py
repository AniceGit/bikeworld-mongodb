import streamlit as st
import time
from src.controllers.utilisateur_controller import inscrire_utilisateur
from pages.sidebar import afficher_sidebar
from src.tools.session import init_session

init_session()

afficher_sidebar()

st.title("Page de d'inscription")
st.write("Bienvenue sur la page d'insciption de BIKEWORLD!")


def inscrire_vue() -> None:
    """
    Affiche le formulaire d'inscription pour un nouvel utilisateur.

    Permet à l'utilisateur de saisir son nom, prénom, téléphone, email et mot de passe.
    Vérifie que tous les champs sont remplis avant d'appeler la fonction d'inscription.
    En cas de succès, attend 2 secondes puis redirige vers la page de connexion.
    Affiche un message d'erreur si des informations sont manquantes.

    Returns:
        None

    Effets de bord:
        Affiche des éléments UI dans Streamlit.
        Appelle la fonction `inscrire_utilisateur` qui affiche elle-même des messages de succès ou d'erreur.
    """
    st.header("Inscription")

    nom = st.text_input("Nom")
    prenom = st.text_input("Prénom")
    tel = st.text_input("Téléphone")
    email = st.text_input("Email")
    mdp = st.text_input("Mot de passe")

    if st.button("💾S'inscrire"):
        if nom and prenom and tel and email and mdp:
            if inscrire_utilisateur(nom, prenom, email, mdp, tel):
                time.sleep(2)
                st.switch_page("pages/connexion.py")
        else:
            st.write("Veuillez saisir vos informations personnelles")


inscrire_vue()
