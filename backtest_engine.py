
import pandas as pd
import numpy as np

def generate_fake_data(periods=100):
    np.random.seed(42)
    prices = np.cumsum(np.random.randn(periods)) + 33600  # centered around US30 area
    timestamps = pd.date_range(end=pd.Timestamp.now(), periods=periods, freq='5min')
    df = pd.DataFrame({'time': timestamps, 'price': prices})
    return df

def calculate_vwap(prices, window=20):
    return prices.rolling(window=window).mean()

def generate_macd(price_series, fast=12, slow=26, signal=9):
    exp1 = price_series.ewm(span=fast, adjust=False).mean()
    exp2 = price_series.ewm(span=slow, adjust=False).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    return macd, signal_line

def backtest_strategy(df):
    df["vwap"] = calculate_vwap(df["price"])
    df["macd"], df["macd_signal"] = generate_macd(df["price"])

    df["round_zone"] = (df["price"] / 100).round() * 100
    df["position"] = "NONE"

    for i in range(1, len(df)):
        # Simple logic: MACD cross + price above/below VWAP + near round number
        macd_cross_up = df.loc[i-1, "macd"] < df.loc[i-1, "macd_signal"] and df.loc[i, "macd"] > df.loc[i, "macd_signal"]
        macd_cross_down = df.loc[i-1, "macd"] > df.loc[i-1, "macd_signal"] and df.loc[i, "macd"] < df.loc[i, "macd_signal"]
        near_round = abs(df.loc[i, "price"] - df.loc[i, "round_zone"]) <= 20

        if macd_cross_up and df.loc[i, "price"] > df.loc[i, "vwap"] and near_round:
            df.loc[i, "position"] = "BUY"
        elif macd_cross_down and df.loc[i, "price"] < df.loc[i, "vwap"] and near_round:
            df.loc[i, "position"] = "SELL"

    return df
