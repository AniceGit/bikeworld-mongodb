import streamlit as st
import json, os, datetime
from src.models.panier import Panier
from models.utilisateur import utilisateur_from_dict


def init_session() -> None:
    if "utilisateur" not in st.session_state:
        if os.path.exists("db/utilisateur_session.json"):
            try:
                with open("db/utilisateur_session.json", "r") as f:
                    data = json.load(f)
                    st.session_state["utilisateur"] = utilisateur_from_dict(data)
            except json.JSONDecodeError:
                # Fichier corrompu ou vide → on le supprime
                os.remove("db/utilisateur_session.json")
                st.session_state["utilisateur"] = None
        else:
            st.session_state["utilisateur"] = None

    if "produit" not in st.session_state:
        st.session_state["produit"] = None

    if "panier" not in st.session_state:
        st.session_state.panier = Panier(str(datetime.date.today()), 0.0)
