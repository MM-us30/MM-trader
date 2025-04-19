
import streamlit as st
import matplotlib.pyplot as plt
from backtest_engine import generate_fake_data, backtest_strategy

def run_backtest_visual():
    st.markdown("### 🧪 Backtest Simulation Results")

    # Generate and backtest
    df = generate_fake_data()
    df = backtest_strategy(df)

    # Count signals
    buy_signals = df[df["position"] == "BUY"].shape[0]
    sell_signals = df[df["position"] == "SELL"].shape[0]

    st.write(f"✅ BUY signals: {buy_signals} | 🔻 SELL signals: {sell_signals}")

    # Plot chart
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df["time"], df["price"], label="Price", color="gray", alpha=0.6)
    ax.plot(df["time"], df["vwap"], label="VWAP", color="blue", linestyle="--", alpha=0.6)
    ax.scatter(df[df["position"] == "BUY"]["time"], df[df["position"] == "BUY"]["price"], label="BUY", marker="^", color="green")
    ax.scatter(df[df["position"] == "SELL"]["time"], df[df["position"] == "SELL"]["price"], label="SELL", marker="v", color="red")

    ax.set_title("MACD + VWAP + Round Number Backtest")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
