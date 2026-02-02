import streamlit as st
import pandas as pd
import json
import plotly.express as px
import geopandas as gpd

st.set_page_config(page_title="Radicalização Brasil", layout="wide")
st.title("Mapa e Dashboard de Radicalização no Brasil")

# --- Carrega dados agregados ---
with open("../data/indicadores_estado.json", "r") as f:
    dados = json.load(f)

df = pd.DataFrame(dados)

# --- Carrega GeoJSON do Brasil (limites dos estados) ---
# Fonte: IBGE ou geojson gratuito
geojson_url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"
brasil_geo = gpd.read_file(geojson_url)

# Plotly exige que o nome do estado no GeoJSON e no DataFrame combinem
# Vamos normalizar os nomes
df['geo'] = df['geo'].str.upper()
brasil_geo['name'] = brasil_geo['name'].str.upper()

# --- Mapa interativo ---
fig_map = px.choropleth_mapbox(
    df,
    geojson=brasil_geo.__geo_interface__,
    locations='geo',
    featureidkey="properties.name",
    color='indice_radicalizacao',
    color_continuous_scale="Reds",
    mapbox_style="carto-positron",
    zoom=3.5,
    center={"lat": -14.2350, "lon": -51.9253},
    opacity=0.7,
    hover_name='geo',
    hover_data={'indice_radicalizacao':True, 'total_posts':True, 'radicalizados':True}
)

st.subheader("Mapa de Radicalização por Estado")
st.plotly_chart(fig_map, use_container_width=True)

# --- Gráfico de barras ---
fig_bar = px.bar(
    df,
    x='geo',
    y='indice_radicalizacao',
    color='indice_radicalizacao',
    labels={'geo':'Estado','indice_radicalizacao':'Índice de Radicalização'},
    color_continuous_scale="Reds"
)
st.subheader("Índice de Radicalização por Estado")
st.plotly_chart(fig_bar, use_container_width=True)

# --- Linha do tempo (simulada) ---
# Criar dataframe simulado de evolução
df_tempo = pd.DataFrame({
    'date': pd.date_range(start='2026-02-01', periods=5),
    'indice_radicalizacao': [0.3,0.35,0.33,0.38,0.36]
})
fig_line = px.line(df_tempo, x='date', y='indice_radicalizacao', markers=True,
                   labels={'date':'Data','indice_radicalizacao':'Índice de Radicalização'})
st.subheader("Evolução do Índice de Radicalização")
st.plotly_chart(fig_line, use_container_width=True)
