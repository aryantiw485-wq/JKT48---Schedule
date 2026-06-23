from datetime import datetime
import requests
import xml.etree.ElementTree as ET

bulan = {
    "Januari": "January",
    "Februari": "February",
    "Maret": "March",
    "April": "April",
    "Mei": "May",
    "Juni": "June",
    "Juli": "July",
    "Agustus": "August",
    "September": "September",
    "Oktober": "October",
    "November": "November",
    "Desember": "December"
}

url = "https://nitter.net/moshi2jkt48/rss"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/rss+xml,application/xml,text/xml,*/*"
}

r = requests.get(url, headers=headers)

root = ET.fromstring(r.text)

items = root.findall(".//item")

for item in items:
    title = item.find("title")

    if title is None:
        continue

    text = title.text

    if "Gita" in text:
    print("⭐ AKAN BUAT EVENT ⭐")
else:
    print("Tidak ada Gita, tidak membuat event.")
