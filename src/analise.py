import pandas as pd
import json
import os
from transformers import pipeline
from datetime import datetime, timedelta
from collections import Counter

# --- Caminho correto ---
DATA_PATH = os.path.join(os.path.dirname(__file__), "../data")

# --- Carregar posts ---
with open(os.path.join(DATA_PATH, "posts.json"), "r") as f:
    posts = json.load(f)

df = pd.DataFrame(posts)

# --- NLP para radicalização ---
classifier = pipeline("sentiment-analysis", model="pierreguillou/bert-base-cased-sentiment")

def medir_radicalizacao(texto):
    resultado = classifier(texto)[0]
    # Label "LABEL_0" = radicalizado, "LABEL_1" = neutro (ajuste conforme modelo)
    return 1 if resultado['label'] == 'LABEL_0' else 0

df['score'] = df['text'].apply(medir_radicalizacao)

# --- Agregação por estado ---
estado_agregado = df.groupby('geo').agg(
    total_posts=('text','count'),
    radicalizados=('score','sum')
).reset_index()
estado_agregado['indice_radicalizacao'] = estado_agregado['radicalizados'] / estado_agregado['total_posts']

# --- Salva indicadores ---
with open(os.path.join(DATA_PATH, "indicadores_estado.json"), "w") as f:
    estado_agregado.to_json(f, orient='records', force_ascii=False, indent=2)

# --- Nuvem de palavras últimas 24h ---
hoje = datetime.now()
ontem = hoje - timedelta(days=1)
df['date'] = pd.to_datetime(df['date'])
df_24h = df[df['date'] >= ontem]

palavras = " ".join(df_24h['text']).lower().split()
stopwords = set(["de","em","o","a","e","do","da","que","para","mais"])
palavras_filtradas = [p for p in palavras if p not in stopwords]
contagem = Counter(palavras_filtradas)

with open(os.path.join(DATA_PATH, "wordcloud_24h.json"), "w") as f:
    json.dump(contagem.most_common(50), f, indent=2)

print("Análise concluída!")