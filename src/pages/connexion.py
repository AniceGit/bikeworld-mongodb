import streamlit as st
import time
from src.controllers.utilisateur_controller import connecter_utilisateur
from pages.sidebar import afficher_sidebar
import base64
from src.tools.session import init_session

init_session()

afficher_sidebar()


def set_bg_image(image_file: str) -> None:
    """
    Définit une image de fond pour l'application Streamlit.

    Args:
        image_file (str): Chemin vers le fichier image (.png ou .jpg) à utiliser en fond.

    Returns:
        None

    Effets de bord:
        Injecte un style CSS dans la page Streamlit pour appliquer l'image en arrière-plan,
        avec des styles pour la taille, la position, la répétition et l'attachement du fond.
        Modifie également la couleur du texte des éléments ciblés pour améliorer la lisibilité.
    """
    with open(image_file, "rb") as image:
        encoded_string = base64.b64encode(image.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/{"png" if image_file.endswith(".png") else "jpg"};base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .custom-title {{
            color: #FFFFFF;  
        }}
        .custom-write {{
            color: #FFFFFF; 
        }}
        .stTextInput>div>div>label {{
            color: #FFFFFF;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# Chemin vers votre image de fond
image_file = "images/fond_velo_noir.jpg"  # Remplacez par le chemin de votre image

# Appliquer le fond d'écran
set_bg_image(image_file)

st.markdown('<h1 class="custom-title">Page de Connexion</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="custom-write">Bienvenue sur la page de connexion de BIKEWORLD!</p>',
    unsafe_allow_html=True,
)


def connexion_vue() -> None:
    """
    Affiche la vue de connexion avec formulaire email/mot de passe.

    Permet à l'utilisateur de saisir ses informations et de tenter de se connecter.

    Returns:
        None

    Effets de bord:
        Affiche un formulaire avec deux champs (email et mot de passe).
        Affiche des messages d'erreur si les champs sont vides.
        Si la connexion réussit, affiche un spinner puis redirige vers la page d'accueil.
    """
    st.markdown('<p class="custom-write">Connexion</p>', unsafe_allow_html=True)

    email = st.text_input("Email")
    mdp = st.text_input("Mot de passe", type="password")

    if st.button("⏻ Se connecter"):
        if email and mdp:
            if connecter_utilisateur(email, mdp):
                with st.spinner(text="Veuillez patienter", show_time=False):
                    time.sleep(2)
                st.switch_page("accueil.py")
        else:
            st.markdown(
                '<p class="custom-write">Veuillez saisir vos informations personnelles</p>',
                unsafe_allow_html=True,
            )

connexion_vue()
