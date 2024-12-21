import streamlit as st
import dask.dataframe as dd
import plotly.express as px
import pandas as pd
import ventes
import shops
import promos
import gdown
import os

# URL de partage Google Drive
file_url = "https://drive.google.com/file/d/1d5v1MI39-Nb6E9xxwd8QYPGserp-96L9/view?usp=sharing"

# Nom local pour enregistrer le fichier CSV
csv_file = "train.csv"

# Télécharger le fichier si nécessaire
if not os.path.exists(csv_file):
    gdown.download(file_url, csv_file, quiet=False)

# Lire le fichier CSV avec Dask
data = dd.read_csv(csv_file)

# Configuration de la page
st.set_page_config(
    page_title="Prédiction des Ventes",
    page_icon="favorita.png",
    layout="wide"
)

# CSS pour changer le style des boutons
custom_css = """
    <style>
    section[data-testid="stSidebar"] div.stButton > button {
        background-color: white !important;
        color: rgb(0, 80, 100) !important;
        text-align: left !important;
        border: none;
        border-radius: 8px;
        font-size: 16px;
        font-weight: bold;
        padding: 8px 12px;
        margin-bottom: 10px;
        cursor: pointer;
        width: 80%;
        font-size: 2rem !important;
    }
    section[data-testid="stSidebar"] div.stButton > button:hover {
        background-color: rgb(0, 80, 100) !important;
        color: white !important;
    }
    .stMultiSelect [data-baseweb="select"] > div {
        border-color: rgb(0, 80, 100) !important;
        color:
    }
    .stMultiSelect [data-baseweb="select"] > div[data-testid="stMarkdownContainer"] > div {
        background-color: rgb(0, 80, 100) !important;
        color: white !important;
    }
    .stMultiSelect [data-baseweb="select"] > div[data-testid="stMarkdownSelect"] > div {
        background-color: rgb(0, 80, 100) !important;
        color: white !important;
    }
    .card {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin: 10px 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .card h2 {
        margin-top: 0;
    }
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ------------------------ Sidebar ------------------------
st.sidebar.title("🛒 Favorita Grocery Stores")

# Gestion des paramètres de navigation avec st.query_params
params = st.experimental_get_query_params()

# Définir les pages avec les boutons
if st.sidebar.button("🏠 Accueil"):
    st.experimental_set_query_params(page="accueil")
if st.sidebar.button("📊 Ventes"):
    st.experimental_set_query_params(page="ventes")
if st.sidebar.button("🎉 Prédictions"):
    st.experimental_set_query_params(page="promotions")


# Récupération de la page active
page = params.get("page", ["accueil"])[0]

st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
""", unsafe_allow_html=True)

# ------------------------ Contenu de la page Accueil ------------------------
data['date'] = dd.to_datetime(data['date'])

def display_accueil():
    last_date = data['date'].max().compute()
    last_date_data = data[data['date'] == last_date]
    total_sales = last_date_data['unit_sales'].sum().compute()
    daily_sales = data.groupby('date')['unit_sales'].sum().compute()
    best_sales = daily_sales.max()
    least_sales = daily_sales.min()

    # Définir les styles CSS pour chaque carte avec icônes
    card_style_1 = """
        <div style="background-color: #4c2a85; padding: 2px; border-radius: 15px; color: white; text-align: center; margin: 2px; ">
            <img src="https://img.icons8.com/color/48/000000/sales-performance.png" alt="Sales Icon" style="width:48px;height:48px;margin-bottom: 5px;"><br>
            <h6 style="margin-bottom: 0px; text-align: center; padding: 0px">Dernière vente</h6>
            <h4 style="margin-up: 0px; text-align: center; padding: 0px; padding-bottom: 2px; ">$%s</h4>
        </div>
    """

    card_style_2 = """
        <div style="background-color: #2a9d8f; padding: 2px; border-radius: 15px; color: white; text-align: center; margin: 2px;">
            <img src="https://img.icons8.com/color/48/000000/money.png" alt="Revenue Icon" style="width:48px;height:48px;">
            <h6 style="margin-bottom: 0px; text-align: center; padding: 0px">Meilleure vente</h6>
            <h4 style="margin-up: 0px; text-align: center; padding: 0px; padding-bottom: 2px; ">$%s</h4>
        </div>
    """

    card_style_3 = """
        <div style="background-color: #D6AC01; padding: 2px; border-radius: 15px; color: white; text-align: center; margin: 2px;">
            <img src="https://img.icons8.com/color/48/000000/money-bag.png" alt="Faible vente" style="width:48px;height:48px;">
            <h6 style="margin-bottom: 0px; text-align: center; padding: 0px">Plus faible vente</h6>
            <h4 style="margin-up: 0px; text-align: center; padding: 0px; padding-bottom: 2px; ">%s</h4>
        </div>
    """

    # Créer trois colonnes
    col1, col2, col3 = st.columns(3)

    # Afficher les cartes dans les colonnes
    with col1:
        st.markdown(card_style_1 % total_sales, unsafe_allow_html=True)

    with col2:
        st.markdown(card_style_2 % best_sales, unsafe_allow_html=True)

    with col3:
        st.markdown(card_style_3 % least_sales, unsafe_allow_html=True)

    # Regrouper les données par date et calculer la somme des ventes pour chaque date
    daily_df = data.groupby('date')['unit_sales'].sum().compute().reset_index()

    # Convertir le DataFrame Dask en DataFrame Pandas pour Plotly
    daily_df = pd.DataFrame(daily_df)
    daily_df = daily_df.sort_values(by='date')

    # Créer le graphique avec Plotly
    fig = px.line(daily_df, x='date', y='unit_sales', title='Sales Overview',
                  labels={'unit_sales': 'Total Sales', 'date': 'Date'}, color_discrete_sequence=['rgb(0, 80, 100)'])

    # Ajouter des annotations pour rendre le graphique plus interactif
    fig.update_traces(mode='lines+markers', marker=dict(size=5))
    fig.update_layout(hovermode='x unified')

    fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',  # Fond transparent
    paper_bgcolor='rgba(0,0,0,0)',  # Fond transparent
    yaxis=dict(
        showgrid=True,  # Masquer la grille verticale
    ),
    xaxis=dict(
        showgrid=False,  # Masquer la grille horizontale
    ) )

    # Afficher le graphique dans Streamlit
    st.plotly_chart(fig)

    # Regrouper les données par date et magasin et calculer la somme des ventes pour chaque date et magasin
    stores_sales = data.groupby(['date', 'store_nbr'])['unit_sales'].sum().compute().reset_index()

    # Convertir le DataFrame Dask en DataFrame Pandas pour Plotly
    stores_sales = pd.DataFrame(stores_sales)

    # Obtenir la liste des magasins uniques
    stores = stores_sales['store_nbr'].unique()

    # Ajouter un widget de sélection de magasin
    selected_store = st.selectbox("Sélectionnez un magasin", stores)

    # Filtrer les données pour le magasin sélectionné
    filtered_data = stores_sales[stores_sales['store_nbr'] == selected_store]

    # Trier les données par date
    filtered_data = filtered_data.sort_values(by='date')

    # Créer le graphique avec Plotly
    fig1 = px.line(filtered_data, x='date', y='unit_sales', title=f'Sales Overview for Store {selected_store}',
                labels={'unit_sales': 'Total Sales', 'date': 'Date'}, color_discrete_sequence=['rgb(0, 80, 100)'])

    # Ajouter des annotations pour rendre le graphique plus interactif
    fig1.update_traces(mode='lines', marker=dict(size=8))
    fig1.update_layout(hovermode='x unified')

    # Ajouter un dégradé de couleur transparent en bas du graphique
    fig1.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Fond transparent
        paper_bgcolor='rgba(0,0,0,0)',  # Fond transparent
        yaxis=dict(
            showgrid=True,  # Masquer la grille verticale
        ),
        xaxis=dict(
            showgrid=False,  # Masquer la grille horizontale
        ),)
    st.plotly_chart(fig1)

# ------------------------ Contenu des pages ------------------------
if page == "accueil":
    st.markdown("<h1 style='display: flex; align-items: center;'><i class='fa-solid fa-house fa-bounce' style='margin-right: 10px;'></i> Accueil</h1>", unsafe_allow_html=True)
    display_accueil()
elif page == "ventes":
    st.title("📊 Analyse des Ventes")
    ventes.display_ventes(data)
elif page == "promotions":
    st.title("🎉Promotions")
    promos.display_promos()
elif page == "boutiques":
    st.title("🏢 Analyse des Boutiques")
    shops.display_shops()

# ------------------------ Footer ------------------------
st.markdown("---")
st.markdown("Développé par **Mouhamadi Bassirou COMPAORE** et **Maty NDIONE**")
