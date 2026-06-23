import requests

r = requests.get("https://example.com")

print("STATUS:", r.status_code)
print("PANJANG:", len(r.text))
