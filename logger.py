
import csv
from datetime import datetime
import os

LOG_FILE = "trade_logs.csv"

def log_trade(action, symbol, price, volume, signal, pnl=None):
    fieldnames = ["time", "action", "symbol", "price", "volume", "signal", "pnl"]

    row = {
        "time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "action": action,
        "symbol": symbol,
        "price": price,
        "volume": volume,
        "signal": signal,
        "pnl": pnl if pnl is not None else ""
    }

    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

def load_trade_logs():
    if not os.path.exists(LOG_FILE):
        return []

    with open(LOG_FILE, mode="r") as file:
        reader = csv.DictReader(file)
        return list(reader)
