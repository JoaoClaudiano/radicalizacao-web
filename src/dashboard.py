import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pydeck as pdk

# ===========================
# Carregamento de dados
# ===========================
st.title("Dashboard Radicalização - Brasil")

with open("dados.json", "r", encoding="utf-8") as f:
    dados = json.load(f)

df = pd.DataFrame(dados)

# ===========================
# Pré-processamento
# ===========================
# Verifica se existe a coluna 'geo'
if 'geo' in df.columns:
    df['geo'] = df['geo'].str.upper()
else:
    st.error("Coluna 'geo' não encontrada nos dados!")

# Converte a coluna de data para datetime
if 'data' in df.columns:
    df['data'] = pd.to_datetime(df['data'])
else:
    st.error("Coluna 'data' não encontrada nos dados!")

# ===========================
# Filtros
# ===========================
estados = df['geo'].unique() if 'geo' in df.columns else []
estado_selecionado = st.multiselect("Selecione o(s) Estado(s):", estados, default=estados)

df_filtered = df[df['geo'].isin(estado_selecionado)] if 'geo' in df.columns else df

# ===========================
# Mapa interativo por estado
# ===========================
st.subheader("Mapa de registros por Estado")
if not df_filtered.empty:
    # Filtra apenas registros com latitude e longitude
    df_mapa = df_filtered.dropna(subset=['lat', 'lon'])
    st.map(df_mapa[['lat', 'lon']])
else:
    st.info("Nenhum registro para o(s) Estado(s) selecionado(s).")

# ===========================
# Ranking de palavras-chave
# ===========================
st.subheader("Ranking de palavras-chave mais citadas")
if 'palavras_chave' in df.columns:
    # Supõe que cada registro tem uma lista de palavras-chave
    todas_palavras = [palavra for lista in df_filtered['palavras_chave'].dropna() for palavra in lista]
    ranking = pd.Series(todas_palavras).value_counts().reset_index()
    ranking.columns = ['Palavra', 'Quantidade']
    st.dataframe(ranking.head(20))
else:
    st.info("Coluna 'palavras_chave' não encontrada.")

# ===========================
# Nuvem de palavras
# ===========================
st.subheader("Nuvem de palavras mais citadas")
if todas_palavras:
    wc = WordCloud(width=800, height=400, background_color='white').generate(" ".join(todas_palavras))
    fig_wc, ax = plt.subplots(figsize=(15, 7))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig_wc)
else:
    st.info("Não há palavras para gerar a nuvem.")

# ===========================
# Evolução temporal por estado
# ===========================
st.subheader("Evolução temporal por Estado")

if not df_filtered.empty:
    df_filtered['data_dia'] = df_filtered['data'].dt.date
    evolucao_dia = df_filtered.groupby(['geo', 'data_dia']).size().reset_index(name='Total')

    fig_evol = px.line(
        evolucao_dia,
        x='data_dia',
        y='Total',
        color='geo',
        markers=True,
        title='Evolução diária de registros por Estado',
        labels={'geo': 'Estado', 'data_dia': 'Data', 'Total': 'Quantidade'}
    )
    st.plotly_chart(fig_evol, use_container_width=True)

    # Evolução horária últimas 24h
    agora = datetime.now()
    ult_24h = agora - timedelta(hours=24)
    df_24h = df_filtered[df_filtered['data'] >= ult_24h]

    if not df_24h.empty:
        df_24h['hora'] = df_24h['data'].dt.hour
        evol_24h = df_24h.groupby(['geo', 'hora']).size().reset_index(name='Total')
        fig_24h = px.line(
            evol_24h,
            x='hora',
            y='Total',
            color='geo',
            markers=True,
            title='Evolução horária últimos 24h por Estado',
            labels={'geo': 'Estado', 'hora': 'Hora', 'Total': 'Quantidade'}
        )
        st.plotly_chart(fig_24h, use_container_width=True)
    else:
        st.info("Nenhum registro nas últimas 24h para os filtros selecionados.")
else:
    st.info("Nenhum registro encontrado para os filtros selecionados.")

# ===========================
# Fim do Dashboard
# ===========================
st.success("Dashboard carregado com sucesso!")