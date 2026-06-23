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

    if "Berikut adalah member yang akan tampil" in text:

        parts = text.split("|")

        show = parts[0].replace(
            "R to @moshi2jkt48: Berikut adalah member yang akan tampil pada pertunjukan",
            ""
        ).strip()

        tanggal = parts[1].strip()

        jam = parts[2].split("WIB")[0].strip()

        for indo, eng in bulan.items():
            tanggal = tanggal.replace(indo, eng)

        waktu = datetime.strptime(
            f"{tanggal} {jam}",
            "%d %B %Y %H.%M"
        )

        print("SHOW :", show)
        print("DATETIME :", waktu)
