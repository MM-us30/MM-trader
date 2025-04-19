
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# CONFIG: spreadsheet and credentials
SPREADSHEET_NAME = "Chameleon_Trade_Logs"
WORKSHEET_NAME = "Live_Trades"

# Load Google Sheets API credentials from a JSON file
def authenticate_gsheets(json_keyfile_path):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_path, scope)
    client = gspread.authorize(creds)
    return client

# Append trade row to sheet
def log_trade_to_sheet(json_keyfile_path, action, symbol, price, volume, signal, pnl=None):
    try:
        client = authenticate_gsheets(json_keyfile_path)
        sheet = client.open(SPREADSHEET_NAME)
        worksheet = sheet.worksheet(WORKSHEET_NAME)
    except Exception:
        # Create if doesn't exist
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
