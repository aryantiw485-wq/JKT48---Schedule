import os

print("DEBUG START")
print(os.environ.keys())
print("DEBUG END")

import os
import json
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build

creds_json = json.loads(os.environ["GOOGLE_CREDENTIALS"])

credentials = service_account.Credentials.from_service_account_info(
    creds_json,
    scopes=["https://www.googleapis.com/auth/calendar"]
)

service = build("calendar", "v3", credentials=credentials)

calendar_id = os.environ["CALENDAR_ID_THEATER"]

event = {
    "summary": "TEST EVENT JKT48 BOT",
    "start": {
        "dateTime": (datetime.utcnow() + timedelta(minutes=1)).isoformat() + "Z",
        "timeZone": "Asia/Jakarta",
    },
    "end": {
        "dateTime": (datetime.utcnow() + timedelta(minutes=61)).isoformat() + "Z",
        "timeZone": "Asia/Jakarta",
    },
}

service.events().insert(calendarId=calendar_id, body=event).execute()

print("TEST EVENT BERHASIL DIBUAT 🫡")
