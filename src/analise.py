import pandas as pd
import json
from transformers import pipeline
from datetime import datetime, timedelta
from collections import Counter

# Carrega dados
with open("../data/posts.json", "r") as f:
    posts = json.load(f)

df = pd.DataFrame(posts)

# --- Hugging Face pipeline (sentiment proxy para radicalização) ---
classifier = pipeline("sentiment-analysis", model="pierreguillou/bert-base-cased-sentiment")

def medir_radicalizacao(texto):
    resultado = classifier(texto)[0]
    if resultado['label'] == 'LABEL_0':  # negativo / crítico
        return 1
    return 0

df['score'] = df['text'].apply(medir_radicalizacao)

# --- Agregação por estado ---
estado_agregado = df.groupby('geo').agg(
    total_posts=('text','count'),
    radicalizados=('score','sum')
).reset_index()
estado_agregado['indice_radicalizacao'] = estado_agregado['radicalizados'] / estado_agregado['total_posts']

with open("../data/indicadores_estado.json", "w") as f:
    estado_agregado.to_json(f, orient='records')

# --- Nuvem de palavras últimas 24h ---
hoje = datetime.now()
ontem = hoje - timedelta(days=1)
df['date'] = pd.to_datetime(df['date'])
df_24h = df[df['date'] >= ontem]

palavras = " ".join(df_24h['text']).lower().split()
stopwords = set(["de","em","o","a","e","do","da","que","para","mais"])
palavras_filtradas = [p for p in palavras if p not in stopwords]
contagem = Counter(palavras_filtradas)

with open("../data/wordcloud_24h.json", "w") as f:
    json.dump(contagem.most_common(50), f, indent=2)

print("Análise concluída!")