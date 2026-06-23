import requests
import xml.etree.ElementTree as ET
import re


TARGET_MEMBER = [
    "Gita",
    "Gita Sekar Andarini"
]


URL = "https://nitter.net/moshi2jkt48/rss"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


print("🔄 Mengambil RSS Moshi...")

response = requests.get(URL, headers=HEADERS, timeout=30)

print("Status RSS:", response.status_code)

if response.status_code != 200:
    print("❌ Gagal mengambil RSS")
    exit()


root = ET.fromstring(response.text)

items = root.findall(".//item")

print("Jumlah item RSS:", len(items))


ada_jadwal = False


for item in items:

    title = item.find("title")

    if title is None:
        continue

    text = title.text or ""


    # hanya cek pengumuman member tampil
    if "Berikut adalah member yang akan tampil" not in text:
        continue


    ada_jadwal = True


    print("\n==========================")
    print("📌 Jadwal ditemukan")
    print("==========================")


    # Ambil member setelah WIB
    member_match = re.search(
        r"WIB\s+(.*)",
        text
    )

    member_list = (
        member_match.group(1)
        if member_match
        else ""
    )


    # Cek Gita
    gita_tampil = any(
        nama.lower() in member_list.lower()
        for nama in TARGET_MEMBER
    )


    # Ambil show
    show = re.search(
        r"pertunjukan (.*?) \|",
        text
    )


    # Ambil tanggal
    tanggal = re.search(
        r"\| (\d{1,2} \w+ \d{4}) \|",
        text
    )


    # Ambil jam
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


    if gita_tampil:
        print("⭐ STATUS : GITA TAMPIL ⭐")
    else:
        print("STATUS : Bukan Gita")


if not ada_jadwal:
    print("\n⚠️ Tidak ada jadwal member ditemukan")
