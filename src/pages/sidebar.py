import streamlit as st


def afficher_sidebar() -> None:
    """
    Affiche la barre latérale de l'application avec des options de navigation.

    Cette fonction affiche différents liens et boutons dans la barre latérale en fonction de l'état de connexion de l'utilisateur.
    Si l'utilisateur n'est pas connecté, des liens pour se connecter et s'inscrire sont affichés.
    Si l'utilisateur est connecté, des liens vers le profil, les commandes, et la déconnexion sont affichés.
    Pour les utilisateurs administrateurs, des liens supplémentaires pour la gestion des commandes et des produits sont affichés.
    Des liens vers le catalogue et le panier sont toujours affichés.
    """

    if st.sidebar.button("🚴🏻 **BikeWorld** 🚴🏻", use_container_width=True):
        st.switch_page("accueil.py")

    if st.session_state["utilisateur"] is None:
        st.sidebar.page_link("pages/connexion.py", label="⏻ Se connecter")
        st.sidebar.page_link("pages/inscription.py", label="S'inscrire")
    else:
        st.sidebar.text(f"Connecté : {st.session_state['utilisateur'].prenom}")
        st.sidebar.page_link("pages/profil.py", label="👤 Profil")
        st.sidebar.page_link("pages/commandes.py", label="📦 Mes commandes")
        st.sidebar.page_link("pages/deconnexion.py", label="⏻ Se déconnecter")
        if st.session_state["utilisateur"].is_admin():
            st.sidebar.text("ADMIN")
            st.sidebar.page_link("pages/admin_commandes.py", label="Admin Commandes")
            st.sidebar.page_link("pages/admin_produits.py", label="Admin Produits")
            st.sidebar.page_link("pages/admin_graph_ventes.py", label="Admin Graph")


    st.sidebar.text("SHOP")
    st.sidebar.page_link("pages/catalogue.py", label="Catalogue")
    st.sidebar.page_link("pages/panier.py", label="Panier")

