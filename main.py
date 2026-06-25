import requests
import xml.etree.ElementTree as ET
import re
import os
import json
from datetime import datetime, timedelta

bulan = {
    "Januari": "01",
    "Februari": "02",
    "Maret": "03",
    "April": "04",
    "Mei": "05",
    "Juni": "06",
    "Juli": "07",
    "Agustus": "08",
    "September": "09",
    "Oktober": "10",
    "November": "11",
    "Desember": "12"
}

def ubah_tanggal(tanggal, jam):

    hari, nama_bulan, tahun = tanggal.split()

    bulan_angka = bulan[nama_bulan]

    jam_baru = jam.replace(".", ":")

    return (
        f"{tahun}-{bulan_angka}-{hari}T"
        f"{jam_baru}:00+07:00"
    )
    
def tambah_2_jam(waktu_iso):

    mulai = datetime.fromisoformat(
        waktu_iso.replace("Z", "+00:00")
    )

    selesai = mulai + timedelta(hours=2)

    return selesai.isoformat()

from google.oauth2 import service_account
from googleapiclient.discovery import build

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

MODE_TEST = False

for item in items:

    if MODE_TEST:

        text = """
Berikut adalah member yang akan tampil pada pertunjukan Sambil Menggandeng Erat Tanganku | 25 Juni 2026 | 19.00 WIB Gita Sekar Andarini, Christy, Lulu
"""

    else:

        title = item.find("title")

        if title is None:
            continue

        text = title.text or ""

        print("RSS:", text)
        
        if "Berikut adalah member yang akan tampil" not in text:
            continue

    print("\n==========================")
    print("📌 Jadwal ditemukan")
    print("==========================")

    member_match = re.search(
        r"WIB\s+(.*)",
        text
    )

    member_list = (
        member_match.group(1)
        if member_match
        else ""
    )

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

    print("Show   :", show.group(1) if show else "-")
    print("Tanggal:", tanggal.group(1) if tanggal else "-")
    print("Jam    :", jam.group(1) if jam else "-")
    print("Member :", member_list)
    print("Apakah Gita dicari? :", ada_gita)

    if ada_gita:

        print("⭐ GITA TAMPIL ⭐")

        judul = f"⭐ GITA TAMPIL - {show.group(1)}"

    else:

        print("📅 Theater tanpa Gita")

        judul = f"JKT48 Theater - {show.group(1)}"


    event_data = {
        "title": judul,
        "date": tanggal.group(1),
        "time": jam.group(1),
        "member": member_list
    }

    print("\n📅 DATA EVENT")
    print(event_data)

    print("\n🚀 Menghubungkan ke Google Calendar...")

    creds_json = json.loads(
            os.environ["GOOGLE_CREDENTIALS"]
        )

    credentials = service_account.Credentials.from_service_account_info(
            creds_json,
            scopes=[
                "https://www.googleapis.com/auth/calendar"
            ]
        )

    service = build(
            "calendar",
            "v3",
            credentials=credentials
        )

    print("✅ Berhasil terhubung ke Google Calendar")

    calendar_id = os.environ["CALENDAR_ID_THEATER"]

    waktu_mulai = ubah_tanggal(
        event_data["date"],
        event_data["time"]
    )


    waktu_selesai = tambah_2_jam(
         waktu_mulai
    )


    event = {
        "summary": event_data["title"],
        "description": event_data["member"],
        "start": {
                "dateTime": waktu_mulai,
                "timeZone": "Asia/Jakarta"
        },
        "end": {
                "dateTime": waktu_selesai,
                "timeZone": "Asia/Jakarta"
        }
    }


    existing_events = service.events().list(
        calendarId=calendar_id,
        q=event_data["title"]
    ).execute()


    event_sudah_ada = False


    for old_event in existing_events.get("items", []):

        old_start = old_event.get("start", {}).get("dateTime")


        if old_start == event["start"]["dateTime"]:

            event_sudah_ada = True
            break



    if event_sudah_ada:

        print("⚠️ Event sudah ada, dilewati")


    else:

        created_event = service.events().insert(
            calendarId=calendar_id,
            body=event
        ).execute()

        print("🎉 EVENT BERHASIL DIBUAT")
        print(created_event["htmlLink"])

    if MODE_TEST:
        break
