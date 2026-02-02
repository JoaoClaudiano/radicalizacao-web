import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px

st.set_page_config(page_title="Dashboard Radicalização", layout="wide")

st.title("Dashboard Radicalização por Estados")

# Caminho do JSON
json_path = "data/posts.json"

# ----------------------------
# 1. Carregando os dados JSON
# ----------------------------
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
# 2. Normaliza a coluna 'geo'
# ----------------------------
if 'geo' not in df.columns:
    df['geo'] = ''

df['geo'] = df['geo'].astype(str).str.upper()

# Substitui valores vazios ou inválidos por "DESCONHECIDO"
df['geo'] = df['geo'].replace({'': 'DESCONHECIDO', 'NA': 'DESCONHECIDO', None: 'DESCONHECIDO'})

# ----------------------------
# 3. Verifica se há dados
# ----------------------------
if df.empty:
    st.warning("O DataFrame está vazio. Nenhum dado para exibir.")
    st.stop()
else:
    st.success(f"Dados carregados com sucesso! Total de registros: {len(df)}")
    st.dataframe(df.head(10))

# ----------------------------
# 4. Agrupamento por estado
# ----------------------------
st.subheader("Contagem de registros por estado")
geo_counts = df['geo'].value_counts().reset_index()
geo_counts.columns = ['Estado', 'Total']

# Tabela
st.table(geo_counts)

# Gráfico de barras
fig = px.bar(geo_counts, x='Estado', y='Total', color='Estado', text='Total')
st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# 5. Mapa interativo por estado
# ----------------------------
# Plotly tem um mapa choropleth de Brasil por sigla
fig_map = px.choropleth(
    geo_counts,
    locations='Estado',
    locationmode='ISO-3166-2',  # usa códigos UF
    color='Total',
    color_continuous_scale='Reds',
    scope='south america',  # ou 'north america' ajustando para Brasil
    labels={'Total': 'Quantidade'},
    title='Distribuição de registros por Estado'
)

fig_map.update_geos(fitbounds="locations", visible=False)
st.plotly_chart(fig_map, use_container_width=True)