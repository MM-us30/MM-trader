import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import streamlit as st
import json

# CONFIG
SPREADSHEET_NAME = "Chameleon_Trade_Logs"
WORKSHEET_NAME = "Live_Trades"

# Authenticate with Streamlit secrets
def authenticate_gsheets_from_secrets():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    service_account_info = json.loads(st.secrets["gcp_service_key"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
    client = gspread.authorize(creds)
    return client

# Log a trade into existing sheet and worksheet
def log_trade_to_sheet(action, symbol, price, volume, signal, pnl=None):
    try:
        client = authenticate_gsheets_from_secrets()
        sheet = client.open(SPREADSHEET_NAME)
        worksheet = sheet.worksheet(WORKSHEET_NAME)
    except Exception as e:
        st.error(f"❌ Google Sheets logging failed: {e}")
        return

    row = [
        datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        action,
        symbol,
        price,
        volume,
        signal,
        pnl if pnl else ""
    ]
    worksheet.append_row(row)
    st.success("✅ Trade logged to Google Sheets successfully!")
