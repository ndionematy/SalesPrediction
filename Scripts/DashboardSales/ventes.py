# ventes.py
import streamlit as st
import dask.dataframe as dd
import pandas as pd
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder

def display_sales_by_state(data):
    state_sales = data.groupby('state')['unit_sales'].sum().compute().reset_index()

    # Calculer le pourcentage de rebond (Bounce) pour chaque état
    total_sales = state_sales['unit_sales'].sum()
    state_sales['bounce'] = (state_sales['unit_sales'] / total_sales) * 100

    # Convertir le DataFrame Dask en DataFrame Pandas pour l'affichage
    state_sales = pd.DataFrame(state_sales)

    # States où on a les meilleures ventes
    state_sales = state_sales.sort_values(by='bounce', ascending=False)
    
    colors1 = px.colors.sample_colorscale("viridis", [n / 5 for n in range(5)])
    bar_sales1 = px.bar(state_sales.head(5), x='state', y='bounce', title='TOP 5 of best states Sales', labels={'bounce': 'Bounce (%)', 'state': 'State'}, color=colors1, color_continuous_scale="viridis")
    bar_sales1.update_layout(showlegend=False)
    st.plotly_chart(bar_sales1)

    colors2 = px.colors.sample_colorscale("Picnic", [n / 5 for n in range(5)])
    bar_sales2 = px.bar(state_sales.tail(5), x='state', y='bounce', title='TOP 5 of worst states Sales', labels={'bounce': 'Bounce (%)', 'state': 'State'}, color=colors2, color_continuous_scale="Picnic")
    bar_sales2.update_layout(showlegend=False)
    st.plotly_chart(bar_sales2)

    # Afficher les données sous forme de tableau interactif
    st.markdown("### Sales by State")
    st.markdown("""
        <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            text-align: center;
            background-color: #f9f9f9;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        </style>
    """, unsafe_allow_html=True)

    # Convertir le DataFrame en HTML
    html = state_sales.to_html(index=False, escape=False)
    st.write(html, unsafe_allow_html=True)
    return state_sales

def plot_selected_states(data, selected_states):
    filtered_data = data[data['state'].isin(selected_states)]

    # Regrouper les données par date et état et calculer la somme des ventes pour chaque date et état
    daily_sales = filtered_data.groupby(['date', 'state'])['unit_sales'].sum().compute().reset_index()

    # Créer le graphique avec Plotly
    fig = px.line(daily_sales, x='date', y='unit_sales', color='state', title='Sales Overview by State',
                  labels={'unit_sales': 'Total Sales', 'date': 'Date'})

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
        )
    )

    # Afficher le graphique dans Streamlit
    st.plotly_chart(fig)

# Fonction pour afficher les ventes par magasin (à utiliser dans le script principal)
def display_ventes(data):
    state_sales = display_sales_by_state(data)

    # Ajouter un widget de sélection multiple pour les états
    selected_states = st.multiselect("Sélectionnez les états", state_sales['state'].unique())

    # Afficher le graphique pour les états sélectionnés
    if selected_states:
        plot_selected_states(data.sort_values(by='date'), selected_states)
