import json
import pandas as pd
from datetime import datetime, timedelta
from geolocalizacao import cidade_para_estado

# --- CARREGAR POSTS ---
with open("../data/posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

df = pd.DataFrame(posts)
df['geo'] = df.get('geo', None)

# Converter cidade/geo para estado
df['geo'] = df['geo'].apply(lambda x: cidade_para_estado(x) if x else "SEM_INFO")

# Criar score de radicalização (simples: palavras-chave)
KEYWORDS = ["extremismo", "radicalização", "ideologia"]  # exemplo
df['score'] = df['text'].apply(lambda t: sum([1 for k in KEYWORDS if k in t.lower()]))

# --- Agregação por estado ---
estado_agregado = df.groupby('geo').agg(
    total_posts=('text','count'),
    radicalizados=('score','sum')
).reset_index()
estado_agregado['indice_radicalizacao'] = estado_agregado['radicalizados'] / estado_agregado['total_posts']

# Salvar JSON para dashboard
estado_agregado.to_json("../data/indicadores_estado.json", orient="records", force_ascii=False)

# --- Posts últimas 24h ---
df['created_at'] = pd.to_datetime(df['created_at'])
hoje = datetime.utcnow()
ultimas_24h = df[df['created_at'] >= hoje - timedelta(hours=24)]
ultimas_24h[['text']].to_json("../data/posts_24h.json", orient="records", force_ascii=False)

print("Análise concluída! JSONs atualizados.")