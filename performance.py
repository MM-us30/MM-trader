
import pandas as pd
from logger import load_trade_logs

def calculate_performance():
    logs = load_trade_logs()
    if not logs:
        return {
            "total_trades": 0,
            "wins": 0,
            "losses": 0,
            "win_rate": 0,
            "net_pnl": 0
        }

    df = pd.DataFrame(logs)
    df["pnl"] = pd.to_numeric(df["pnl"], errors="coerce").fillna(0)

    total_trades = len(df)
    wins = df[df["pnl"] > 0].shape[0]
    losses = df[df["pnl"] < 0].shape[0]
    net_pnl = df["pnl"].sum()
    win_rate = (wins / total_trades) * 100 if total_trades > 0 else 0

    return {
        "total_trades": total_trades,
        "wins": wins,
        "losses": losses,
        "win_rate": round(win_rate, 2),
        "net_pnl": round(net_pnl, 2)
    }
