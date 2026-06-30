import requests
import xml.etree.ElementTree as ET
import re
import os
import json
import requests
from datetime import datetime, timedelta

from google.oauth2 import service_account
from googleapiclient.discovery import build

# =====================================
# TELEGRAM
# =====================================

TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


def kirim_telegram(pesan):

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    response = requests.post(
        url,
        json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": pesan
        },
        timeout=30
    )

    print("Status Telegram:", response.status_code)
    print(response.text)


# ===== TES TELEGRAM =====
kirim_telegram("🎉 Tes notifikasi dari GitHub Actions berhasil!")


# =====================================
# BULAN INDONESIA
# =====================================

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


# =====================================
# KONVERSI TANGGAL
# =====================================

def ubah_tanggal(tanggal, jam):

    hari, nama_bulan, tahun = tanggal.split()

    return (
        f"{tahun}-{bulan[nama_bulan]}-{hari.zfill(2)}T"
        f"{jam.replace('.', ':')}:00+07:00"
    )


# =====================================
# TAMBAH DURASI 2 JAM
# =====================================

def tambah_2_jam(waktu_iso):

    mulai = datetime.fromisoformat(waktu_iso)

    selesai = mulai + timedelta(hours=2)

    return selesai.isoformat()


# =====================================
# GOOGLE CALENDAR
# =====================================

print("🔗 Menghubungkan Google Calendar...")

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

calendar_id = os.environ["CALENDAR_ID_THEATER"]

print("✅ Google Calendar siap")



# =====================================
# RSS MOSHI
# =====================================

print("🔄 Mengambil RSS Moshi...")

rss_url = "https://nitter.net/moshi2jkt48/rss"

response = requests.get(
    rss_url,
    headers={
        "User-Agent": "Mozilla/5.0"
    },
    timeout=30
)

print("Status RSS:", response.status_code)

root = ET.fromstring(response.text)

items = root.findall(".//item")

print("Jumlah item RSS:", len(items))


# =====================================
# PROSES RSS
# =====================================

for item in items:

    title = item.find("title")

    if title is None:
        continue

    text = title.text or ""

    if "Berikut adalah member yang akan tampil" not in text:
        continue

    print("\n======================")
    print("📌 JADWAL DITEMUKAN")
    print("======================")

    print(text)

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

    member_match = re.search(
        r"WIB\s+(.*)",
        text
    )

    if not (show and tanggal and jam):

        print("⚠️ Format tweet tidak cocok")
        continue

    member_list = (
        member_match.group(1)
        if member_match
        else ""
    )

    nama_show = show.group(1)

    ada_gita = (
        "gita"
        in member_list.lower()
    )

    warna = "8"

    if "Sambil Menggandeng Erat Tanganku" in nama_show:
        warna = "10"

    elif "Pertaruhan Cinta" in nama_show:
        warna = "11"

    elif "Aturan Anti Cinta" in nama_show:
        warna = "9"

    elif "Cara Meminum Ramune" in nama_show:
        warna = "5"
        

    waktu_mulai = ubah_tanggal(
        tanggal.group(1),
        jam.group(1)
    )

    waktu_selesai = tambah_2_jam(
        waktu_mulai
    )

    event = {
        "summary": judul,
        "description": (
            f"Show : {nama_show}\n\n"
            f"Member:\n{member_list}"
        ),
        "colorId": warna,
        "start": {
             "dateTime": waktu_mulai,
             "timeZone": "Asia/Jakarta"
        },
        "end": {
            "dateTime": waktu_selesai,
            "timeZone": "Asia/Jakarta"
        },
        "reminders": {
             "useDefault": False,
             "overrides": [
                 {
                     "method": "popup",
                     "minutes": 1440
                 },
                 {
                    "method": "popup",
                    "minutes": 60
                 }
             ]
         }
      }

    existing_events = service.events().list(
        calendarId=calendar_id,
        maxResults=2500
    ).execute()

    event_ditemukan = False

    for old_event in existing_events.get(
        "items",
        []
    ):

        old_start = (
            old_event.get(
                "start",
                {}
            ).get(
                "dateTime"
            )
        )

        old_summary = (
            old_event.get(
                "summary",
                ""
            )
        )

        if (
            old_start == waktu_mulai
            and
            nama_show.lower()
            in old_summary.lower()
        ):

            service.events().update(
                calendarId=calendar_id,
                eventId=old_event["id"],
                body=event
            ).execute()

            print("🔄 Event diperbarui")
            print(judul)

            event_ditemukan = True
            break

if not event_ditemukan:

   created = service.events().insert(
       calendarId=calendar_id,
       body=event
   ).execute()

   print("🎉 Event baru dibuat")
   print(created["htmlLink"])

if ada_gita:

    pesan = (
        "🌸 GITA ALERT 🌸\n\n"
        f"🎭 {nama_show}\n"
        f"📅 {tanggal.group(1)}\n"
        f"🕒 {jam.group(1)} WIB\n\n"
        "✅ Sudah masuk Google Calendar"
    )

else:

    pesan = (
        "📅 Jadwal Theater Baru\n\n"
        f"🎭 {nama_show}\n"
        f"📅 {tanggal.group(1)}\n"
        f"🕒 {jam.group(1)} WIB"
    )

kirim_telegram(pesan)
print("\n✅ Sinkronisasi selesai")
