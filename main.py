import requests

url = "https://nitter.net/moshi2jkt48/rss"

r = requests.get(url)

print("STATUS:", r.status_code)
print("PANJANG:", len(r.text))

print(r.text[:1000])
