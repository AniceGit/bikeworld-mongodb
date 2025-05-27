import streamlit as st
from controllers.produit_controller import get_top_3_ventes
from models.produit import Produit, afficher_image_stock
from src.tools.session import init_session

init_session()

def afficher_produits_stars() -> None:
    """
    Affiche les trois produits les plus vendus dans une interface Streamlit.

    Cette fonction récupère les trois produits les plus vendus et les affiche
    dans une grille de colonnes avec des médailles pour indiquer leur rang.
    Chaque produit est affiché avec son image, son nom, son prix, et un bouton
    pour voir les détails du produit.
    """
    
    st.markdown("#")
    st.markdown(
    "<h2 style='text-align: center; color: #f1ab00; background-color: #191919;'>Top Ventes</h2>",
    unsafe_allow_html=True)
    st.markdown("#")
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