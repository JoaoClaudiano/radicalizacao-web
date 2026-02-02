import pandas as pd
from collections import Counter
import json

# Carrega dados
with open("../data/posts.json", "r") as f:
    posts = json.load(f)

df = pd.DataFrame(posts)

# --- Função simples de "radicalização" ---
def medir_radicalizacao(texto):
    """Simples scoring de radicalização baseado em palavras-chave"""
    palavras_radicais = ["besteira", "radical", "conspirações", "ódio", "violência"]
    score = sum(1 for palavra in palavras_radicais if palavra.lower() in texto.lower())
    return score

df['score'] = df['text'].apply(medir_radicalizacao)

# Agregação por estado
estado_agregado = df.groupby('geo').agg(
    total_posts=('text','count'),
    radicalizados=('score','sum')
).reset_index()

estado_agregado['indice_radicalizacao'] = estado_agregado['radicalizados'] / estado_agregado['total_posts']

print(estado_agregado)

# Salva dados agregados
estado_agregado.to_json("../data/indicadores_estado.json", orient='records')
