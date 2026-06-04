import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Ambil credentials dari GitHub Secrets
creds_json = json.loads(os.environ["GOOGLE_CREDENTIALS"])

credentials = service_account.Credentials.from_service_account_info(
    creds_json,
    scopes=["https://www.googleapis.com/auth/calendar"]
)

service = build("calendar", "v3", credentials=credentials)

print("Bot kalender JKT48 siap jalan 🫡")
