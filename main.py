import requests

url = "https://nitter.net/moshi2jkt48"

r = requests.get(
    url,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
)

print("STATUS:", r.status_code)
print("PANJANG HALAMAN:", len(r.text))
print(r.text[:500])
