import streamlit as st
from pages.sidebar import afficher_sidebar
from tools.session import init_session
from pages.bikeworld import afficher_produits_stars
import base64
from src.tools.session import init_session
import os

init_session()

# Affichage wide forcé
st.set_page_config(layout="wide")

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# st.set_page_config(layout="wide")
def set_bg_image(image_file: str):
    """
    Définit une image de fond pour l'application Streamlit.

    Args:
        image_file (str): Chemin vers le fichier image à utiliser comme fond d'écran.
    """
    # Ajout du logo dans une div
    logo_path = os.path.join('images', 'logo_bikeworld_fond_blanc.png')
    if os.path.exists(logo_path):
        logo_base64 = image_to_base64(logo_path)
        st.markdown(
            f"""
            <div style='text-align: center;'>
                <img src='data:image/png;base64,{logo_base64}' alt='Logo' style='width: auto;'>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.error("Le fichier du logo n'existe pas.")

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
        </style>
        """,
        unsafe_allow_html=True,
    )

# Chemin vers votre image de fond
image_file = (
    "images/catalogue_background.jpg"  # Remplacez par le chemin de votre image
)

# Appliquer le fond d'écran
set_bg_image(image_file)

def afficher_accueil():
    """
    Affiche la page d'accueil de l'application.

    Cette fonction initialise la session, affiche la barre latérale et les produits vedettes.
    """
    init_session()
    afficher_sidebar()
    afficher_produits_stars()

#Fonction appelée pour afficher la page d'accueil
afficher_accueil()
