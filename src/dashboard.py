import streamlit as st
import pandas as pd
import json
import plotly.express as px
import geopandas as gpd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(page_title="Radicalização Brasil", layout="wide")
st.title("Dashboard de Radicalização no Brasil")

# --- Dados por estado ---
with open("../data/indicadores_estado.json", "r") as f:
    dados = json.load(f)
df = pd.DataFrame(dados)
df['geo'] = df['geo'].str.upper()

# --- GeoJSON Brasil ---
geojson_url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"
brasil_geo = gpd.read_file(geojson_url)
brasil_geo['name'] = brasil_geo['name'].str.upper()

# --- Mapa ---
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

# --- Linha do tempo simulada (substituir futuramente por dados reais) ---
df_tempo = pd.DataFrame({
    'date': pd.date_range(end=pd.Timestamp.now(), periods=5),
    'indice_radicalizacao': [0.3,0.35,0.33,0.38,0.36]
})
fig_line = px.line(df_tempo, x='date', y='indice_radicalizacao', markers=True,
                   labels={'date':'Data','indice_radicalizacao':'Índice de Radicalização'})
st.subheader("Evolução do Índice de Radicalização")
st.plotly_chart(fig_line, use_container_width=True)

# --- Nuvem de palavras últimas 24h ---
with open("../data/wordcloud_24h.json", "r") as f:
    word_counts = dict(json.load(f))

wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_counts)
st.subheader("Palavras mais comuns nas últimas 24h")
fig_wc, ax = plt.subplots(figsize=(12,6))
ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")
st.pyplot(fig_wc)