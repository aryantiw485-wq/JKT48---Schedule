import requests
import xml.etree.ElementTree as ET
import re


TARGET_MEMBER = [
    "Gita",
    "Gita Sekar Andarini"
]


url = "https://nitter.net/moshi2jkt48/rss"

headers = {
    "User-Agent": "Mozilla/5.0"
}


r = requests.get(url, headers=headers)

root = ET.fromstring(r.text)

items = root.findall(".//item")


for item in items:

    title = item.find("title")

    if title is None:
        continue

    text = title.text


    if "Berikut adalah member yang akan tampil" not in text:
        continue


    # Ambil bagian setelah WIB (daftar member)
    member_list = text.split("WIB")[-1]


    ada_gita = any(
        nama in member_list
        for nama in TARGET_MEMBER
    )


    if ada_gita:

        show = re.search(
            r"pertunjukan (.*?) \|",
            text
        )

        tanggal = re.search(
            r"\| (\d{1,2} \w+ \d{4}) \|",
            text
        )

        jam = re.search(
            r"\| (\d{2}\.\d{2}) WIB",
            text
        )


        print("⭐ GITA TAMPIL ⭐")
        print("Show   :", show.group(1))
        print("Tanggal:", tanggal.group(1))
        print("Jam    :", jam.group(1))
