import pandas as pd
import json

# Carrega dados
with open("../data/posts.json", "r") as f:
    posts = json.load(f)

df = pd.DataFrame(posts)

# Score de radicalização simples
def medir_radicalizacao(texto):
    palavras_radicais = ["besteira", "radical", "conspirações", "ódio", "violência"]
    return sum(1 for palavra in palavras_radicais if palavra.lower() in texto.lower())

df['score'] = df['text'].apply(medir_radicalizacao)

# Agregação por estado
estado_agregado = df.groupby('geo').agg(
    total_posts=('text','count'),
    radicalizados=('score','sum')
).reset_index()

estado_agregado['indice_radicalizacao'] = estado_agregado['radicalizados'] / estado_agregado['total_posts']

# Salva dados
estado_agregado.to_json("../data/indicadores_estado.json", orient='records')
print("Indicadores salvos!")
