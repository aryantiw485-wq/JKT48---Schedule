import requests
import xml.etree.ElementTree as ET
import re


MODE_TEST = True


# Nama yang dicari
TARGET_MEMBER = [
    "Gita",
    "Gita Sekar Andarini"
]


URL = "https://nitter.net/moshi2jkt48/rss"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


print("🔄 Mengambil RSS Moshi...")


response = requests.get(
    URL,
    headers=HEADERS,
    timeout=30
)


print("Status RSS:", response.status_code)


root = ET.fromstring(response.text)

items = root.findall(".//item")


print("Jumlah item RSS:", len(items))


for item in items:

    title = item.find("title")

    if title is None:
        continue


text = title.text or ""

print("RSS:", text)


 # Cari tweet daftar member
if "Berikut adalah member yang akan tampil" not in text:
    continue


    print("\n==========================")
    print("📌 Jadwal ditemukan")
    print("==========================")


    # Ambil daftar member
    member_match = re.search(
        r"WIB\s+(.*)",
        text
    )


    if member_match:
        member_list = member_match.group(1)
    else:
        member_list = ""


    # Cek Gita
    ada_gita = any(nama.lower() in member_list.lower()
        for nama in TARGET_MEMBER)


    # MODE LATIHAN
    if MODE_TEST:
        ada_gita = True


    # Ambil show
    show = re.search(
        r"pertunjukan (.*?) \|",text)


    # Ambil tanggal
    tanggal = re.search(
        r"\| (\d{1,2} \w+ \d{4}) \|",text)


    # Ambil jam
    jam = re.search(r"\| (\d{2}\.\d{2}) WIB",text)


    print("Show   :",show.group(1) if show else "-")

    print("Tanggal:",tanggal.group(1) if tanggal else "-")

    print("Jam    :",jam.group(1) if jam else "-")

    print("Member :",member_list)


    print("Apakah Gita dicari? :",ada_gita)


    if ada_gita:
        print("⭐ GITA TAMPIL ⭐")

        event_data = {
            "title": f"⭐ JKT48 Theater - {show.group(1)}",
            "date": tanggal.group(1),
            "time": jam.group(1),
            "member": member_list}

        print("\n📅 DATA EVENT")
        print(event_data)

    else:
        print("❌ Bukan Gita")
