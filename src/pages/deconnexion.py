import streamlit as st
import time
from pages.sidebar import afficher_sidebar
from src.controllers.utilisateur_controller import deconnecter_utilisateur
from src.tools.session import init_session

init_session()

afficher_sidebar()

def deconnexion_vue() -> None:
    """
    Gère la déconnexion de l'utilisateur.

    Fonctionnalités :
    - Appelle la fonction `deconnecter_utilisateur` pour déconnecter l'utilisateur courant.
    - Si un utilisateur était connecté, affiche un message de succès avec son prénom,
      puis redirige vers la page d'accueil après un délai de 2 secondes.
    - Si aucun utilisateur n'était connecté, affiche un message d'information adapté.

    Ne retourne rien, affiche directement la page Streamlit.
    """
    prenom = deconnecter_utilisateur()
    if prenom is not None:
        with st.spinner(text="Veuillez patienter", show_time=False):
            st.success(f"Au revoir {prenom} !")
            time.sleep(2)
        st.switch_page("accueil.py")
    else:
        st.info("Vous n'étiez pas connecté")

deconnexion_vue()
