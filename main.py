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

for item in items:
    title = item.find("title")

    if title is not None:
        text = title.text

        if "gita" in text.lower():
            print("=== DITEMUKAN GITA ===")
            print(text)
            print()
