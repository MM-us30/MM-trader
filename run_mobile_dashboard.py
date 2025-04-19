import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import random

symbol = "US30"
current_price = round(random.uniform(33500, 33700), 2)
vwap_value = current_price - random.uniform(-20, 20)
macd_signal = random.choice(["BUY", "SELL", "NEUTRAL"])
round_number_zone = round(round(current_price / 100) * 100)

st.set_page_config(page_title="Chameleon Dashboard", layout="centered")
st.markdown("<h1 style='text-align: center;'>Chameleon Trading Dashboard</h1>", unsafe_allow_html=True)

st.subheader(f"Symbol: {symbol}")
st.markdown(f"**Current Price:** {current_price}")
st.markdown(f"**Nearest Round Number:** {round_number_zone}")
st.markdown(f"**VWAP:** {round(vwap_value, 2)}")
st.markdown(f"**MACD Signal:** {macd_signal}")

st.markdown("### MACD/VWAP Heatmap")
heatmap_data = np.random.randn(15, 15)
fig, ax = plt.subplots()
cax = ax.imshow(heatmap_data, cmap='RdYlGn', aspect='auto')
ax.set_xticks([])
ax.set_yticks([])
st.pyplot(fig)

st.markdown("### Last Signals")
log_data = pd.DataFrame({
    "Time": pd.date_range(datetime.datetime.now() - datetime.timedelta(minutes=75), periods=5, freq='15T'),
    "Signal": ["BUY", "SELL", "BUY", "SELL", "BUY"],
    "Price": np.random.uniform(33500, 33700, 5).round(2)
})
st.table(log_data)

st.markdown("### Controls")
col1, col2 = st.columns(2)
with col1:
    st.button("Start Chameleon Bot")
with col2:
    st.button("Pause Bot")

st.markdown("### Position & PnL")
st.metric(label="Open Position", value="BUY 1.0 lot")
st.metric(label="Current PnL", value="+$124.67")

st.caption("Built for mobile-first control and trade confidence using the Chameleon Logic.")
