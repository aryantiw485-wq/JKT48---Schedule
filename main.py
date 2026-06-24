import requests
import xml.etree.ElementTree as ET
import re
import os
import json

from datetime import datetime, timedelta

from google.oauth2 import service_account
from googleapiclient.discovery import build


MODE_TEST = True

TARGET_MEMBER = [
    "Gita",
    "Gita Sekar Andarini"
]


print("🔄 Mengambil RSS Moshi...")

response = requests.get(
    "https://nitter.net/moshi2jkt48/rss",
    headers={"User-Agent": "Mozilla/5.0"},
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

    if "Berikut adalah member yang akan tampil" not in text:
        continue

    print("📌 Tweet member list ditemukan")

    member_match = re.search(
        r"WIB\s+(.*)",
        text
    )

    member_list = (
        member_match.group(1)
        if member_match
        else ""
    )

    ada_gita = any(
        nama.lower() in member_list.lower()
        for nama in TARGET_MEMBER
    )

    if MODE_TEST:
        ada_gita = True

    print("Apakah Gita dicari? :", ada_gita)

    if not ada_gita:
        continue

    print("⭐ GITA TAMPIL ⭐")

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

    calendar_id = os.environ[
        "CALENDAR_ID_THEATER"
    ]

    event = {
        "summary": "⭐ JKT48 Theater TEST",
        "start": {
            "dateTime":
                (datetime.utcnow() + timedelta(minutes=1)).isoformat() + "Z",
            "timeZone": "Asia/Jakarta"
        },
        "end": {
            "dateTime":
                (datetime.utcnow() + timedelta(minutes=61)).isoformat() + "Z",
            "timeZone": "Asia/Jakarta"
        }
    }

    service.events().insert(
        calendarId=calendar_id,
        body=event
    ).execute()

    print("📅 EVENT BERHASIL DIBUAT")

    break
