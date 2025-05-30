import streamlit as st
import pandas as pd
import plotly.express as px
from controllers.produit_controller import get_produits

def afficher_graph_produits():
    st.title("Statistiques Ventes par produit")

    produits = get_produits

    if not produits:
        st.write("Aucun produit trouvé")
    else:
        data =[]

        #DataFrame Pandas
        for produit in produits:
            data.append({
                "ID": produit.id,
                "Nom": produit.nom,
                "Ventes": produit.ventes,
            })

        df = pd.DataFrame(data)

afficher_graph_produits()