import streamlit as st
st.set_page_config(page_title="Chameleon Dashboard", layout="centered")
from dashboard_ui import show_performance_panel
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import random
from backtest_viz import run_backtest_visual
from backtest_toggle import run_toggle_backtest_visual
from dashboard_ui import show_performance_panel
# Simulated values (will be replaced by real MT5 data later)
symbol = "US30"
current_price = round(random.uniform(33500, 33700), 2)
vwap_value = current_price - random.uniform(-20, 20)
macd_signal = random.choice(["BUY", "SELL", "NEUTRAL"])
round_number_zone = round(round(current_price / 100) * 100)
st.markdown("<h1 style='text-align: center;'>Chameleon Trading Dashboard</h1>", unsafe_allow_html=True)
st.image("signal_heatmap_v2.png", caption="MACD/VWAP Signal Heatmap", use_container_width=True)
show_performance_panel()

# Signal overview section
st.subheader(f"Symbol: {symbol}")
st.markdown(f"**Current Price:** {current_price}")
st.markdown(f"**Nearest Round Number:** {round_number_zone}")
st.markdown(f"**VWAP:** {round(vwap_value, 2)}")
st.markdown(f"**MACD Signal:** {macd_signal}")

# Signal log
st.markdown("### Last Signals")
log_data = pd.DataFrame({
    "Time": pd.date_range(datetime.datetime.now() - datetime.timedelta(minutes=75), periods=5, freq='15T'),
    "Signal": ["BUY", "SELL", "BUY", "SELL", "BUY"],
    "Price": np.random.uniform(33500, 33700, 5).round(2)
})
st.table(log_data)

# Bot controls
st.markdown("### Controls")
col1, col2 = st.columns(2)
with col1:
    st.button("Start Chameleon Bot")
with col2:
    st.button("Pause Bot")

# Position and PnL tracking
st.markdown("### Position & PnL")
st.metric(label="Open Position", value="BUY 1.0 lot")
st.metric(label="Current PnL", value="+$124.67")

run_backtest_visual()
run_toggle_backtest_visual()

# Footer
st.caption("Built for mobile-first control and trade confidence using the Chameleon Logic.")
