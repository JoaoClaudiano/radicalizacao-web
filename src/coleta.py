import json

# Simulação de coleta de dados
novos_posts = [
    {"text": "O país precisa de mais diálogo!", "source":"twitter", "date":"2026-02-03", "geo":"São Paulo"},
    {"text": "Radicais estão exagerando.", "source":"reddit", "date":"2026-02-03", "geo":"Minas Gerais"}
]

# Adiciona aos dados existentes
with open("../data/posts.json", "r") as f:
    posts = json.load(f)

posts.extend(novos_posts)

with open("../data/posts.json", "w") as f:
    json.dump(posts, f, indent=2)

print("Novos posts adicionados!")
