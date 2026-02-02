import streamlit as st
import pandas as pd
import geopandas as gpd
import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="Dashboard Radicalização Avançado", layout="wide")
st.title("Dashboard Radicalização Avançado")

# ----------------------------
# 1. Carregando dados JSON
# ----------------------------
json_path = "data/posts.json"
with open(json_path, "r", encoding="utf-8") as f:
    dados = json.load(f)

df = pd.DataFrame(dados)

# Normaliza colunas
df['geo'] = df.get('geo', '').astype(str).str.upper().replace({'': 'DESCONHECIDO', 'NA': 'DESCONHECIDO'})
df['data'] = pd.to_datetime(df.get('data', None), errors='coerce')
df['texto'] = df.get('texto', '').astype(str)

# ----------------------------
# 2. Sidebar filtros
# ----------------------------
st.sidebar.header("Filtros")
estados_disponiveis = df['geo'].unique().tolist()
estados_selecionados = st.sidebar.multiselect("Estados", estados_disponiveis, default=estados_disponiveis)

ult_24h_checkbox = st.sidebar.checkbox("Últimas 24h", value=True)
palavra_filtro = st.sidebar.text_input("Filtrar por palavra-chave/hashtag")

df_filtered = df[df['geo'].isin(estados_selecionados)]
if palavra_filtro.strip():
    df_filtered = df_filtered[df_filtered['texto'].str.contains(palavra_filtro, case=False)]

# ----------------------------
# 3. Mapas reais do Brasil
# ----------------------------
st.subheader("Mapa interativo por Estado")

# Carrega shapefile Brasil (UFs)
shapefile_path = "data/BR_UF_2023.shp"  # baixado do IBGE ou geojson oficial
gdf = gpd.read_file(shapefile_path)
gdf['UF'] = gdf['SIGLA']  # coluna UF deve existir no shapefile

# Conta registros por estado
estado_counts = df_filtered['geo'].value_counts().reset_index()
estado_counts.columns = ['UF', 'Total']

# Junta com GeoDataFrame
gdf = gdf.merge(estado_counts, on='UF', how='left').fillna(0)

# Plot interativo Plotly
fig_map = px.choropleth(
    gdf,
    geojson=gdf.geometry,
    locations=gdf.index,
    color='Total',
    hover_name='UF',
    hover_data={'Total': True},
    color_continuous_scale='Reds',
    labels={'Total': 'Quantidade'}
)
fig_map.update_geos(fitbounds="locations", visible=False)
st.plotly_chart(fig_map, use_container_width=True)

# ----------------------------
# 4. Ranking palavras-chave por estado
# ----------------------------
st.subheader("Ranking de palavras-chave por Estado")
from collections import Counter

if not df_filtered.empty:
    all_text = ' '.join(df_filtered['texto'])
    palavras = [p.lower() for p in all_text.split() if len(p) > 3]  # filtra palavras pequenas
    ranking = Counter(palavras).most_common(20)
    df_ranking = pd.DataFrame(ranking, columns=['Palavra', 'Ocorrências'])
    st.table(df_ranking)

    # Nuvem de palavras
    st.subheader("Nuvem de palavras-chave")
    wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate(all_text)
    plt.figure(figsize=(15, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)
else:
    st.info("Nenhum registro encontrado para os filtros selecionados.")

# ----------------------------
# 5. Tendência últimas 24h
# ----------------------------
if ult_24h_checkbox:
    st.subheader("Tendência últimas 24h")
    agora = datetime.now()
    ult_24h = agora - timedelta(hours=24)
    df_24h = df_filtered[df_filtered['data'] >= ult_24h]
    if not df_24h.empty:
        trend_counts = df_24h.groupby(df_24h['data'].dt.hour).size().reset_index(name='Total')
        fig_trend = px.line(trend_counts, x='data', y='Total', markers=True, title='Posts últimas 24h por hora')
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("Nenhum registro nas últimas 24h para os filtros selecionados.")