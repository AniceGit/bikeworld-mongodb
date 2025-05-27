import streamlit as st
import time
from pages.sidebar import afficher_sidebar
from models.utilisateur import Utilisateur
from models.adresse import Adresse
from controllers.utilisateur_controller import creer_adresse, get_adresses_utilisateur, sauvegarder_json_utilisateur, supprimer_adresse_utilisateur
from src.tools.session import init_session

init_session()

# Affichage sidebar et titre
afficher_sidebar()
st.title("Ajout d'une nouvelle adresse")
if st.button("↩️ Profil"):
    st.switch_page("pages/profil.py")

# Récupération des infos de l'utilisateur connecté
utilisateur: Utilisateur = st.session_state["utilisateur"]

# Input (on les vide au changement de page)
numero = st.text_input("Numéro")
type_voie = st.text_input("Type de voie")
nom_voie = st.text_input("Nom de voie")
code_postal = st.text_input("Code Postal")
ville = st.text_input("Ville")
pays = st.text_input("Pays")

# On affecte les valeurs insérées au nouvel utilisateur et on le modifie en db, session et json puis on refresh la page
if st.button("➕ Ajouter"):
    if numero and type_voie and nom_voie and code_postal and ville and pays:
        if creer_adresse(
            numero, type_voie, nom_voie, code_postal, ville, pays, 0, 1, utilisateur.id
        ):
            with st.spinner(text="Veuillez patienter", show_time=False):
                time.sleep(2)
            st.switch_page("pages/profil.py")
    else:
        st.write("Veuillez saisir votre adresse complète")

# On récupère toutes les adresses liées à cet utilisateur et on les met dans une liste
adresses: list[Adresse] = get_adresses_utilisateur(utilisateur.id)
option = st.selectbox(
    "Choisissez parmi vos adresses",
    (adresse.__str__() for adresse in adresses),
    index=None,
    placeholder="Choisir...",
)

if option is None :
     button_delete_disabled = True
else:
    adresse_selectionnee = next(
        (adresse for adresse in adresses if adresse.__str__() == option), None
    )
    button_delete_disabled = False

if st.button("❌ Supprimer adresse", disabled=button_delete_disabled):
    id_adresse_a_supprimer = adresse_selectionnee.id
    supprimer_adresse_utilisateur(id_adresse_a_supprimer, utilisateur)
    
    if utilisateur.adresse is not None and id_adresse_a_supprimer == utilisateur.adresse.id:
        nouvel_utilisateur = utilisateur
        nouvel_utilisateur.adresse = None
        sauvegarder_json_utilisateur(nouvel_utilisateur)
    with st.spinner(text="Veuillez patienter", show_time=False):
        time.sleep(2)
        st.switch_page("pages/profil.py")
