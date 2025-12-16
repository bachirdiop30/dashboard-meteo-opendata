# main.py - Dashboard météo amélioré
import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Chargement des données
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned/meteo_cleaned.csv")
    # Conversion en datetime si nécessaire
    if df['datetime'].dtype == 'O':
        df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
    return df

df = load_data()

# -----------------------------
# Sidebar - filtres interactifs
# -----------------------------
st.sidebar.title("Filtres du dashboard")

# Filtre département
departements = st.sidebar.multiselect(
    "Sélectionner le(s) département(s)",
    options=df['departement'].unique(),
    default=df['departement'].unique()
)
df_filtered = df[df['departement'].isin(departements)]

# Filtre station
stations = st.sidebar.multiselect(
    "Sélectionner la station",
    options=df_filtered['station_name'].unique(),
    default=df_filtered['station_name'].unique()
)
df_filtered = df_filtered[df_filtered['station_name'].isin(stations)]

# Filtre date
start_date = st.sidebar.date_input("Date de début", df_filtered['datetime'].min().date())
end_date = st.sidebar.date_input("Date de fin", df_filtered['datetime'].max().date())
df_filtered = df_filtered[(df_filtered['datetime'].dt.date >= start_date) &
                          (df_filtered['datetime'].dt.date <= end_date)]

# Variable à visualiser
variable = st.sidebar.selectbox(
    "Variable à visualiser",
    options=["temperature", "wind_speed", "humidity"]
)

# -----------------------------
# Titre
# -----------------------------
st.title("📊 Dashboard Météo-France")
st.subheader(f"Variable sélectionnée : {variable.capitalize()}")

# -----------------------------
# Carte interactive
# -----------------------------
# Sécuriser la taille des points pour éviter NaN ou négatifs
df_filtered['size_var'] = df_filtered[variable].fillna(0).clip(lower=0) + 0.1

fig_map = px.scatter_mapbox(
    df_filtered,
    lat="lat",
    lon="lon",
    hover_name="station_name",
    hover_data=[variable, 'datetime'],
    color=variable,
    size='size_var',
    zoom=5,
    height=500,
    color_continuous_scale="Viridis"
)
fig_map.update_layout(mapbox_style="open-street-map")
fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig_map, width='stretch')

# -----------------------------
# Histogramme horaire
# -----------------------------
df_hist = df_filtered.groupby("hour")[variable].mean().reset_index()
fig_hist = px.bar(
    df_hist,
    x="hour",
    y=variable,
    labels={"hour": "Heure", variable: f"Moyenne {variable}"},
    title=f"{variable.capitalize()} moyen par heure"
)
st.plotly_chart(fig_hist, width='stretch')

# -----------------------------
# Histogramme par station
# -----------------------------
df_station = df_filtered.groupby("station_name")[variable].mean().reset_index()
fig_station = px.bar(
    df_station,
    x="station_name",
    y=variable,
    labels={"station_name": "Station", variable: f"Moyenne {variable}"},
    title=f"{variable.capitalize()} moyen par station"
)
st.plotly_chart(fig_station, width='stretch')
