import json
import pandas as pd
from datetime import datetime, timedelta

# --- Carregar posts coletados ---
with open("../data/posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

df = pd.DataFrame(posts)

# Garantir coluna geo
if 'geo' not in df.columns:
    df['geo'] = None
df['geo'] = df['geo'].fillna("SEM_INFO")

# Garantir coluna score de radicalização
if 'score' not in df.columns:
    df['score'] = 0.0

# --- Agregação por estado ---
estado_agregado = df.groupby('geo').agg(
    total_posts=('text','count'),
    radicalizados=('score','sum')
).reset_index()

estado_agregado['indice_radicalizacao'] = estado_agregado['radicalizados'] / estado_agregado['total_posts']

# --- Salvar indicadores por estado ---
estado_agregado.to_json("../data/indicadores_estado.json", orient="records", force_ascii=False)

# --- Posts das últimas 24h ---
hoje = datetime.utcnow()
df['created_at'] = pd.to_datetime(df['created_at'])
ultimas_24h = df[df['created_at'] >= hoje - timedelta(hours=24)]

# --- Salvar posts recentes para nuvem de palavras ---
ultimas_24h[['text']].to_json("../data/posts_24h.json", orient="records", force_ascii=False)

print("Análise concluída! JSONs atualizados.")