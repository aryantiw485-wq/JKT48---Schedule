import requests
import xml.etree.ElementTree as ET
import re

print("🔄 Mengambil RSS Moshi...")

URL = "https://nitter.net/moshi2jkt48/rss"

response = requests.get(
    URL,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=30
)

print("Status RSS:", response.status_code)

root = ET.fromstring(response.text)
items = root.findall(".//item")

print("Jumlah item RSS:", len(items))

MODE_TEST = True

for item in items:

    title = item.find("title")

    if title is None:
        continue

    if MODE_TEST:
        text = """
Berikut adalah member yang akan tampil pada pertunjukan Sambil Menggandeng Erat Tanganku | 25 Juni 2026 | 19.00 WIB Gita Sekar Andarini, Christy, Lulu
"""
        MODE_TEST = False
    else:
        continue

    print("\n==========================")
    print("📌 Jadwal ditemukan")
    print("==========================")

    member_match = re.search(
        r"WIB\s+(.*)",
        text
    )

    if member_match:
        member_list = member_match.group(1)
    else:
        member_list = ""

    ada_gita = "gita" in member_list.lower()

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

    print(
        "Show   :",
        show.group(1) if show else "-"
    )

    print(
        "Tanggal:",
        tanggal.group(1) if tanggal else "-"
    )

    print(
        "Jam    :",
        jam.group(1) if jam else "-"
    )

    print(
        "Member :",
        member_list
    )

    print(
        "Apakah Gita dicari? :",
        ada_gita
    )
if ada_gita:
    print("⭐ GITA TAMPIL ⭐")

    event_data = {
        "title": f"⭐ JKT48 Theater - {show.group(1)}",
        "date": tanggal.group(1),
        "time": jam.group(1),
        "member": member_list
    }

    print("\n📅 DATA EVENT")
    print(event_data)

    print("\n🚀 Mencoba membuat event kalender...")

else:
    print("❌ Bukan Gita")
