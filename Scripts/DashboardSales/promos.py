import streamlit as st
import ventes
import os
import gdown
import dask.dataframe as dd

file_url = "https://drive.google.com/uc?export=download&id=1d5v1MI39-Nb6E9xxwd8QYPGserp-96L9"

# Nom local pour enregistrer le fichier CSV
csv_file = "train_model_Final.csv"

if not os.path.exists(csv_file):
    gdown.download(file_url, csv_file, quiet=False)

new_data = dd.read_csv(csv_file)

def display_promos():
    st.markdown("<h2>Prédiction</h2>", unsafe_allow_html=True)
    # Ajoutez ici votre code pour afficher les promotions
    state_sales = ventes.display_sales_by_state(new_data)

    # Ajouter un widget de sélection multiple pour les états
    selected_states = st.multiselect("Sélectionnez les états", state_sales['state'].unique())

    # Afficher le graphique pour les états sélectionnés
    if selected_states:
       ventes. plot_selected_states(new_data.sort_values(by='date'), selected_states)

