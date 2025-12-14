import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Chargement des données
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned/meteo_cleaned.csv")
    return df

df = load_data()

# -----------------------------
# Sidebar - filtres interactifs
# -----------------------------
st.sidebar.title("Filtres")

departements = st.sidebar.multiselect(
    "Sélectionner le(s) département(s)",
    options=df['departement'].unique(),
    default=df['departement'].unique()
)

df_filtered = df[df['departement'].isin(departements)]

stations = st.sidebar.multiselect(
    "Sélectionner la station",
    options=df_filtered['station_name'].unique(),
    default=df_filtered['station_name'].unique()
)
df_filtered = df_filtered[df_filtered['station_name'].isin(stations)]

variable = st.sidebar.selectbox(
    "Variable à visualiser",
    options=["temperature", "wind_speed", "humidity"]
)

# -----------------------------
# Préparer la taille des points
# -----------------------------
# Remplacer les NaN par 0 et prendre valeurs absolues
size_column = df_filtered[variable].fillna(0).abs()
# Échelle minimale pour que les points soient visibles
size_column = size_column + 0.1

# -----------------------------
# Titre
# -----------------------------
st.title("Dashboard Météo-France")
st.subheader(f"Variable sélectionnée : {variable.capitalize()}")

# -----------------------------
# Carte interactive
# -----------------------------
fig_map = px.scatter_mapbox(
    df_filtered,
    lat="lat",
    lon="lon",
    hover_name="station_name",
    hover_data=[variable],
    color=variable,
    size=size_column,
    zoom=5,
    height=500,
    color_continuous_scale="Viridis"
)
fig_map.update_layout(mapbox_style="open-street-map")
fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig_map, use_container_width=True)

# -----------------------------
# Histogramme horaire
# -----------------------------
df_hist = df_filtered.groupby("hour")[variable].mean().reset_index()
fig_hist = px.bar(
    df_hist,
    x="hour",
    y=variable,
    labels={"hour": "Heure", variable: f"Moyenne {variable}"},
    title=f"{variable.capitalize()} moyen par heure",
    color=variable,
    color_continuous_scale="Viridis"
)
st.plotly_chart(fig_hist, use_container_width=True)
