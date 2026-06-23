import requests
import xml.etree.ElementTree as ET

url = "https://nitter.net/moshi2jkt48/rss"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/rss+xml,application/xml,text/xml,*/*"
}

r = requests.get(url, headers=headers)

root = ET.fromstring(r.text)

items = root.findall(".//item")

print("Jumlah item:", len(items))
print()

for i, item in enumerate(items[:20], start=1):
    title = item.find("title")

    print("=" * 50)
    print(f"ITEM {i}")

    if title is not None:
        print(title.text[:300])

    print()
