import streamlit as st
from controllers.produit_controller import get_top_3_ventes
from models.produit import Produit, afficher_image_stock
from src.tools.session import init_session

init_session()

def afficher_produits_stars() -> None:
    """
    Affiche les trois produits les plus vendus dans une interface Streamlit.

    Cette fonction récupère les trois produits les plus vendus à l'aide de la fonction
    `get_top_3_ventes` et les affiche dans une grille de colonnes. Chaque produit est
    présenté avec une médaille indiquant son rang (or pour le premier, argent pour le
    deuxième, et bronze pour le troisième). Les informations affichées pour chaque produit
    incluent son image, son nom, son prix, et un bouton pour accéder à une page de détails
    spécifique au produit.

    Les produits sont disposés dans une interface utilisateur attrayante avec des styles
    CSS personnalisés pour les éléments de texte et les images. Si un produit n'a pas d'image,
    un message "Aucune image disponible" est affiché à la place.

    Returns:
        None: Cette fonction ne retourne rien mais modifie l'interface utilisateur Streamlit
              directement en affichant les produits.

    Raises:
        Exception: Peut lever des exceptions liées à l'accès aux données des produits ou à
                   l'interface Streamlit, bien que celles-ci ne soient pas explicitement
                   gérées dans la fonction.
    """

    liste_top_ventes: list[Produit] = get_top_3_ventes()
        
    nb_colonnes = 3
    colonnes = st.columns(nb_colonnes)

         # Parcourir les produits et le top 3 des ventes
    for i, produit in enumerate(liste_top_ventes):
        column_index = i % nb_colonnes
        with colonnes[column_index]:
            if produit.image:
                # colonnes pour aligner le nom et le bouton
                nom_col, button_col = st.columns([3, 1])
                with nom_col:
                    medaille = ""
                    if i == 0:
                        medaille = "🥇"
                    elif i == 1:
                        medaille ="🥈"
                    else: medaille = "🥉"
                    st.markdown(
                    f"""
                    <div style='background-color: #191919; padding: 4px; border-radius: 5px;'>
                        <p style='font-size: 19px; font-weight: bold; color: #f1ab00; margin: 0;'>{medaille} {produit.nom}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.image(produit.image, use_container_width=True)
                #with nom_col:
                st.markdown(
                        f"""
                            <div style='background-color: #191919; padding: 1px; border-radius: 5px;'>
                                <p style='font-size: 23px; margin: 0'>Prix: {produit.prix:.2f} €</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                )
                with button_col:
                    if st.button("Détail", key=produit.id):
                        st.session_state["produit"] = produit
                        st.switch_page("pages/produit.py")

                st.markdown(
                        f"""
                        <div style='background-color: #191919; padding: 4px; border-radius: 5px;'>
                            <p style='font-size: 20px; font-weight: bold; color: #f1ab00; margin: 0;'>{afficher_image_stock(produit.stock)}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                st.markdown("#")
            else:
                st.write("Aucune image disponible")