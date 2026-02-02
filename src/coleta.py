import requests
import json
import os
from datetime import datetime

# --- Caminho correto para data ---
DATA_PATH = os.path.join(os.path.dirname(__file__), "../data")
os.makedirs(DATA_PATH, exist_ok=True)

# --- Twitter/X Bearer Token ---
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAI5q7QEAAAAAgY6kUhPI0%2BHs5gGsDyZBWWTLfDg%3DYlk7xA1x5SqyqBgkAdkn5wlsi4YMeELNdgnzOgvjL8eIeWB9xY"

def coletar_tweets(query="radicalismo OR extremismo", max_results=50):
    url = "https://api.twitter.com/2/tweets/search/recent"
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    params = {
        "query": query + " lang:pt -is:retweet",
        "max_results": max_results,
        "tweet.fields": "created_at,geo"
    }
    res = requests.get(url, headers=headers, params=params)
    if res.status_code != 200:
        print(f"Erro Twitter API: {res.status_code}")
        return []
    data = res.json().get("data", [])
    tweets = []
    for t in data:
        geo = t.get("geo", {}).get("place_id", None)
        tweets.append({
            "text": t["text"],
            "source": "twitter",
            "date": t["created_at"],
            "geo": geo
        })
    return tweets

# --- Executa coleta ---
print("Coletando tweets do Twitter/X...")
todos_posts = coletar_tweets(max_results=50)

# --- Salva JSON ---
with open(os.path.join(DATA_PATH, "posts.json"), "w") as f:
    json.dump(todos_posts, f, indent=2)

print(f"Coleta concluída! Total de posts: {len(todos_posts)}")