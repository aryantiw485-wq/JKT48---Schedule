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

ditemukan = False

for item in items:
    title = item.find("title")

    if title is None:
        continue

    text = title.text

    if (
        "Berikut adalah member yang akan tampil" in text
        and "Gita" in text
    ):
        ditemukan = True

        print("⭐ GITA DITEMUKAN ⭐")
        print(text)
        print()

if not ditemukan:
    print("Belum ada member list yang berisi Gita di 20 posting terakhir.")
