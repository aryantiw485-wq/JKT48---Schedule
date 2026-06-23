import requests

url = "https://nitter.net/moshi2jkt48"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/137.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "en-US,en;q=0.9"
}

r = requests.get(url, headers=headers, timeout=30)

print("STATUS:", r.status_code)
print("URL AKHIR:", r.url)
print("HEADERS:", r.headers.get("content-type"))
print("PANJANG HALAMAN:", len(r.text))

print("ISI AWAL:")
print(repr(r.text[:300]))
