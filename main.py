import requests

url = "https://nitter.net/moshi2jkt48/rss"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/137.0 Safari/537.36",
    "Accept": "application/rss+xml,application/xml,text/xml,*/*",
    "Accept-Language": "en-US,en;q=0.9"
}

r = requests.get(url, headers=headers, timeout=30)

print("STATUS:", r.status_code)
print("PANJANG:", len(r.text))
print("CONTENT:", repr(r.text[:200]))
