import requests
import xml.etree.ElementTree as ET
import re


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


    # hanya ambil tweet daftar member
    if "Berikut adalah member yang akan tampil" not in text:
        continue


    print("\n======================")
    print("DATA DITEMUKAN")
    print("======================")


    # Ambil nama show
    show = re.search(
        r"pertunjukan (.*?) \|",
        text
    )

    if show:
        nama_show = show.group(1)
    else:
        nama_show = "Tidak diketahui"


    # Ambil tanggal
    tanggal = re.search(
        r"\| (\d{1,2} \w+ \d{4}) \|",
        text
    )

    if tanggal:
        tanggal_show = tanggal.group(1)
    else:
        tanggal_show = "Tidak diketahui"


    # Ambil jam
    jam = re.search(
        r"\| (\d{2}\.\d{2}) WIB",
        text
    )

    if jam:
        jam_show = jam.group(1)
    else:
        jam_show = "Tidak diketahui"


    # Cek Gita
    if "Gita" in text:
        status = "⭐ GITA TAMPIL"
    else:
        status = "Bukan Gita"


    print("Show   :", nama_show)
    print("Tanggal:", tanggal_show)
    print("Jam    :", jam_show)
    print("Status :", status)
