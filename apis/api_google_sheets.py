import os

import gspread
from google.oauth2.service_account import Credentials

CREDENTIALS_FILE = os.path.join(os.getcwd(), "apis", "credentials.json")

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=scopes)
client = gspread.authorize(creds)

sheet_id = ""
sheet = client.open_by_key(sheet_id)

print(sheet.sheet1.get_all_values())
