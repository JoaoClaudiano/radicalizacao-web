import requests
import praw
import feedparser
import json
from datetime import datetime

# ---------- 1️⃣ Twitter/X ----------
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

# ---------- 2️⃣ Reddit ----------
reddit = praw.Reddit(
    client_id="SEU_CLIENT_ID",
    client_secret="SEU_CLIENT_SECRET",
    user_agent="radicalizacao_web"
)

def coletar_reddit(subreddits=["brasil","politica"], limit=50):
    posts = []
    for sub in subreddits:
        for submission in reddit.subreddit(sub).new(limit=limit):
            posts.append({
                "text": submission.title + " " + submission.selftext,
                "source": "reddit",
                "date": datetime.fromtimestamp(submission.created_utc).strftime("%Y-%m-%d %H:%M:%S"),
                "geo": None
            })
    return posts

# ---------- 3️⃣ RSS de blogs ----------
def coletar_rss(urls):
    posts = []
    for rss_url in urls:
        feed = feedparser.parse(rss_url)
        for entry in feed.entries:
            posts.append({
                "text": entry.title + " " + getattr(entry, "summary", ""),
                "source": "rss",
                "date": getattr(entry, "published", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                "geo": None
            })
    return posts

# ---------- 4️⃣ Executa coleta ----------
todos_posts = []

print("Coletando Twitter...")
todos_posts.extend(coletar_tweets(max_results=50))

print("Coletando Reddit...")
todos_posts.extend(coletar_reddit(limit=50))

print("Coletando RSS...")
rss_feeds = ["https://g1.globo.com/rss/g1/politica/"]
todos_posts.extend(coletar_rss(rss_feeds))

# ---------- 5️⃣ Salva em posts.json ----------
with open("../data/posts.json", "w") as f:
    json.dump(todos_posts, f, indent=2)

print(f"Coleta finalizada! Total de posts: {len(todos_posts)}")