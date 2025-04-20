
import streamlit as st
import json

def authenticate_gsheets_from_secrets():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    service_account_info = json.loads(st.secrets["gcp_service_key"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
    client = gspread.authorize(creds)
    return client


# Append trade row to sheet
def log_trade_to_sheet(json_keyfile_path, action, symbol, price, volume, signal, pnl=None):
    client = authenticate_gsheets_from_secrets()


    try:
        sheet = client.open(SPREADSHEET_NAME)
        worksheet = sheet.worksheet(WORKSHEET_NAME)
    except Exception:
        # Create sheet if it doesn't exist
        sheet = client.create(SPREADSHEET_NAME)
        worksheet = sheet.sheet1
        worksheet.update_title(WORKSHEET_NAME)
        worksheet.append_row(["Time", "Action", "Symbol", "Price", "Volume", "Signal", "PnL"])

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
