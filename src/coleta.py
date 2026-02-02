import requests
import json

# --- CONFIGURAÇÃO ---
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAI5q7QEAAAAAgY6kUhPI0%2BHs5gGsDyZBWWTLfDg%3DYlk7xA1x5SqyqBgkAdkn5wlsi4YMeELNdgnzOgvjL8eIeWB9xY"
QUERY = "radicalização OR extremismo OR ideologia"  # exemplo de busca
MAX_RESULTS = 50  # por request

def coletar_posts():
    url = "https://api.twitter.com/2/tweets/search/recent"
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    params = {
        "query": QUERY,
        "max_results": MAX_RESULTS,
        "tweet.fields": "created_at,geo,text,author_id",
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print("Erro na coleta:", response.text)
        return []

    dados = response.json().get("data", [])
    print(f"{len(dados)} posts coletados do X")
    return dados

if __name__ == "__main__":
    posts = coletar_posts()
    with open("../data/posts.json", "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)