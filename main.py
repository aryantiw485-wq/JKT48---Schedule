from datetime import datetime
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

ada_gita = False

for item in items:
    title = item.find("title")

    if title is not None:
        print(title.text)
        
    text = title.text

    if "Gita" in text:
        ada_gita = True
        print("⭐ AKAN BUAT EVENT ⭐")
        print(text)

if not ada_gita:
    print("Tidak ada Gita, tidak membuat event.")
