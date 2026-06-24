import requests
import xml.etree.ElementTree as ET
import re
import os
import json

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

MODE_TEST = True

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

        event_data = {
            "title": f"⭐ JKT48 Theater - {show.group(1)}",
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

        event = {
            "summary": event_data["title"],
            "description": event_data["member"],
            "start": {
                "dateTime": "2026-06-25T19:00:00+07:00",
                "timeZone": "Asia/Jakarta"
            },
            "end": {
                "dateTime": "2026-06-25T21:00:00+07:00",
                "timeZone": "Asia/Jakarta"
            }
        }

        existing_events = service.events().list(
            calendarId=calendar_id,
            q=event_data["title"]
        ).execute()

        if existing_events.get("items"):

            print("⚠️ Event sudah ada, dilewati")

        else:

            created_event = service.events().insert(
                calendarId=calendar_id,
                body=event
            ).execute()

            print("🎉 EVENT BERHASIL DIBUAT")
            print(created_event["htmlLink"])

    else:

        print("❌ Bukan Gita")

    if MODE_TEST:
        break
