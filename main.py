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

item = items[0]

for child in item:
    print("TAG:", child.tag)
    print("ISI:", str(child.text)[:500])
    print("-" * 50)
