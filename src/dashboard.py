import streamlit as st
import pandas as pd
import json
import plotly.express as px

st.set_page_config(page_title="Radicalização Brasil", layout="wide")

# Carrega dados agregados
with open("../data/indicadores_estado.json", "r") as f:
    dados = json.load(f)

df = pd.DataFrame(dados)

st.title("Mapa e Dashboard de Radicalização no Brasil")

# --- Mapa ---
fig_map = px.choropleth(
    df,
    locations="geo",
    locationmode="USA-states",  # temporário para teste
    color="indice_radicalizacao",
    hover_name="geo",
    color_continuous_scale="Reds",
    labels={'indice_radicalizacao':'Índice de Radicalização'}
)
st.plotly_chart(fig_map, use_container_width=True)

# --- Gráfico de barras ---
fig_bar = px.bar(df, x='geo', y='indice_radicalizacao', color='indice_radicalizacao',
                 labels={'geo':'Estado','indice_radicalizacao':'Índice de Radicalização'})
st.plotly_chart(fig_bar, use_container_width=True)
