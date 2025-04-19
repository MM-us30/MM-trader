
import os
import pandas as pd
from logger import load_trade_logs

# Configurable parameters
MAX_DAILY_LOSS = -500  # Adjust to your comfort level

def should_pause_trading():
    logs = load_trade_logs()
    if not logs:
        return False

    df = pd.DataFrame(logs)
    df["pnl"] = pd.to_numeric(df["pnl"], errors="coerce").fillna(0)
    df["time"] = pd.to_datetime(df["time"])
    today = pd.Timestamp.utcnow().normalize()

    # Filter only today's trades
    today_trades = df[df["time"] >= today]
    total_loss_today = today_trades["pnl"].sum()

    return total_loss_today <= MAX_DAILY_LOSS

def get_daily_loss():
    logs = load_trade_logs()
    if not logs:
        return 0

    df = pd.DataFrame(logs)
    df["pnl"] = pd.to_numeric(df["pnl"], errors="coerce").fillna(0)
    df["time"] = pd.to_datetime(df["time"])
    today = pd.Timestamp.utcnow().normalize()
    today_trades = df[df["time"] >= today]
    return today_trades["pnl"].sum()
