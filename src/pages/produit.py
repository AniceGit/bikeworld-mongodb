import streamlit as st
from pages.sidebar import afficher_sidebar
from controllers.produit_controller import get_details_produit
from models.produit import afficher_image_stock
from src.tools.session import init_session
import base64
from pymongo import MongoClient

#Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["bikeworld-mongo"]  
collection = db["produit"]

init_session()
afficher_sidebar()
id = st.session_state["produit"].id
produit = get_details_produit(id)

def set_bg_image(image_file: str) -> None:
    """
    Définit une image de fond pour l'application Streamlit.

    Args:
        image_file (str): Chemin vers le fichier image à utiliser comme fond d'écran.
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
            color: #000000;  
        }}
        .custom-write {{
            color: #000000; 
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# Chemin vers votre image de fond
image_file = "images/fond_detail.jpg"  # Remplacez par le chemin de votre image

# Appliquer le fond d'écran
set_bg_image(image_file)

st.title(produit.nom)

col1, col2 = st.columns([1, 2])
with col1:
    if produit.image:
        st.image(produit.image, caption=produit.nom, use_container_width=True)
    else:
        st.write("Aucune image disponible")
    with col2:
        st.write(
            f"<span style='font-size: 21px; color: #f1ab00;'>**Description**</span>:",
            unsafe_allow_html=True,
        )
        st.write(f"🚲  {produit.description}", unsafe_allow_html=True)
        st.write(
            f"<span style='font-size: 21px;color: #f1ab00'>**Spécifications Techniques**</span>:",
            unsafe_allow_html=True,
        )
        st.write(f"🛠️ {produit.spec_tech}")
        st.write(
            f"<span style='font-size: 21px;color: #f1ab00'>**Couleur**</span>: {produit.couleur}",
            unsafe_allow_html=True,
        )
        st.write(
            f"<span style='font-size: 21px;color: #f1ab00'>**Prix**</span>: {produit.prix:.2f} €",
            unsafe_allow_html=True,
        )
        st.markdown(
                        f"""
                            <p style='font-size: 20px; font-weight: bold; color: #f1ab00; margin: 0;'>{afficher_image_stock(produit.stock)}</p>
                        """,
                        unsafe_allow_html=True
                    )
        st.markdown("#")
        if st.button("Ajouter au panier", key=produit.id):
            panier = st.session_state.panier
            if panier:
                for produit_quantite in panier.liste_produits_quantite:
                    p_id = produit_quantite["produit_id"]

                    if p_id == produit.id:
                        if produit_quantite["quantite"] + 1 > produit.stock:
                            st.error(
                                f"Stock insuffisant pour le produit {produit.nom} !"
                            )
                            break
                        else:
                            produit_quantite["quantite"] += 1
                            panier.total_panier += produit.prix
                            paniertotal_panier = round(panier.total_panier, 2)
                            produit_quantite["total"] = (
                                produit.prix * produit_quantite["quantite"]
                            )
                            produit_quantite["total"] = round(
                                produit_quantite["total"], 2
                            )
                            st.session_state.panier = panier
                            st.success(f"{produit.nom} a été ajouté au panier !")
                            break

                else:
                    if produit.stock == 0:
                        st.error(f"Stock insuffisant pour le produit {produit.nom} !")
                    else:
                        panier.total_panier += produit.prix
                        panier.total_panier = round(panier.total_panier, 2)
                        panier.liste_produits_quantite.append(
                            {
                                "produit_id": produit.id,
                                "produit": produit.nom,
                                "quantite": 1,
                                "prix": produit.prix,
                                "total": produit.prix,
                                "desc": produit.description,
                                "spec_tech": produit.spec_tech,
                                "couleur": produit.couleur,
                                "image": produit.image
                            }
                        )
                        st.session_state.panier = panier
                        st.success(f"{produit.nom} a été ajouté au panier !")
