import streamlit as st
import pandas as pd
import json
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="Dashboard Radicalização", layout="wide")

st.title("Dashboard Radicalização")

# ----------------------------
# 1. Carregando os dados JSON
# ----------------------------
json_path = "data/posts.json"

if not os.path.exists(json_path):
    st.error(f"Arquivo JSON não encontrado: {json_path}")
    st.stop()

with open(json_path, "r", encoding="utf-8") as f:
    try:
        dados = json.load(f)
    except json.JSONDecodeError:
        st.error("Erro ao ler o JSON. Verifique o formato do arquivo.")
        st.stop()

df = pd.DataFrame(dados)

# ----------------------------
# 2. Normaliza colunas
# ----------------------------
if 'geo' not in df.columns:
    df['geo'] = ''
df['geo'] = df['geo'].astype(str).str.upper()
df['geo'] = df['geo'].replace({'': 'DESCONHECIDO', 'NA': 'DESCONHECIDO', None: 'DESCONHECIDO'})

# Converte coluna de data (assume que existe 'data' no formato ISO: YYYY-MM-DD HH:MM:SS)
if 'data' in df.columns:
    df['data'] = pd.to_datetime(df['data'], errors='coerce')
else:
    df['data'] = pd.NaT

# ----------------------------
# 3. Filtros interativos
# ----------------------------
st.sidebar.header("Filtros")
estados_disponiveis = df['geo'].unique().tolist()
estados_selecionados = st.sidebar.multiselect("Estados", estados_disponiveis, default=estados_disponiveis)

df_filtered = df[df['geo'].isin(estados_selecionados)]

# ----------------------------
# 4. Contagem por estado
# ----------------------------
st.subheader("Contagem de registros por estado")
geo_counts = df_filtered['geo'].value_counts().reset_index()
geo_counts.columns = ['Estado', 'Total']
st.table(geo_counts)

fig_bar = px.bar(geo_counts, x='Estado', y='Total', color='Estado', text='Total')
st.plotly_chart(fig_bar, use_container_width=True)

# ----------------------------
# 5. Mapa interativo
# ----------------------------
fig_map = px.choropleth(
    geo_counts,
    locations='Estado',
    locationmode='ISO-3166-2',
    color='Total',
    color_continuous_scale='Reds',
    scope='south america',
    labels={'Total': 'Quantidade'},
    title='Distribuição de registros por Estado'
)
fig_map.update_geos(fitbounds="locations", visible=False)
st.plotly_chart(fig_map, use_container_width=True)

# ----------------------------
# 6. Nuvem de palavras-chave
# ----------------------------
st.subheader("Nuvem de palavras-chave mais citadas")

if 'texto' in df_filtered.columns:
    all_text = ' '.join(df_filtered['texto'].dropna().astype(str))
    if all_text.strip():
        wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate(all_text)
        plt.figure(figsize=(15, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        st.pyplot(plt)
    else:
        st.info("Não há textos para gerar a nuvem de palavras.")
else:
    st.info("Coluna 'texto' não encontrada no dataset.")

# ----------------------------
# 7. Tendência últimas 24h
# ----------------------------
st.subheader("Tendência últimas 24h")
if 'data' in df_filtered.columns:
    agora = datetime.now()
    ult_24h = agora - timedelta(hours=24)
    df_24h = df_filtered[df_filtered['data'] >= ult_24h]

    if not df_24h.empty:
        trend_counts = df_24h.groupby(df_24h['data'].dt.hour).size().reset_index(name='Total')
        fig_trend = px.line(trend_counts, x='data', y='Total', markers=True, title='Posts nas últimas 24h por hora')
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("Nenhum registro nas últimas 24 horas.")
else:
    st.info("Coluna 'data' não encontrada no dataset.")