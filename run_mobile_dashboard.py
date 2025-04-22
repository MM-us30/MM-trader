import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import random
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

# --- CONFIGURATION ---
st.set_page_config(page_title="Chameleon Dashboard", layout="centered")

# --- SESSION STATE INIT ---
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()

# --- HEADER ---
st.markdown("<h1 style='text-align: center;'>🦎 Chameleon Trading Dashboard</h1>", unsafe_allow_html=True)

# --- REFRESH CONTROLS ---
st.sidebar.header("🔄 Refresh Options")
auto_refresh = st.sidebar.toggle("Auto-refresh", value=True)
refresh_interval = st.sidebar.selectbox("Refresh interval (minutes):", [1, 2, 5, 10], index=2)

if st.sidebar.button("🔁 Manual Refresh"):
    st.rerun()

# --- AUTO REFRESH LOGIC ---
if auto_refresh and time.time() - st.session_state.last_refresh > refresh_interval * 60:
    st.session_state.last_refresh = time.time()
    st.rerun()

# --- AUTH ---
def authenticate_gsheets_from_upload():
    uploaded_file = st.file_uploader("🔐 Upload your Google JSON key", type=["json"])

    if uploaded_file is not None:
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        try:
            content = json.load(uploaded_file)
            st.write("📄 JSON parsed successfully.")

            scope = [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive"
            ]
            creds = ServiceAccountCredentials.from_json_keyfile_dict(content, scope)
            client = gspread.authorize(creds)
            st.success("✅ Google Sheets authenticated successfully.")
            return client
        except Exception as e:
            st.error(f"❌ Failed to authenticate: {e}")
            st.exception(e)
    else:
        st.info("📥 Please upload your JSON key to enable Google Sheets logging.")
    return None

# --- SIMULATED DATA ---
symbol = "US30"
current_price = round(random.uniform(33500, 33700), 2)
vwap_value = current_price - random.uniform(-20, 20)
macd_signal = random.choice(["BUY", "SELL", "NEUTRAL"])
round_number_zone = round(round(current_price / 100) * 100)

# --- SIGNAL OVERVIEW ---
st.subheader(f"Symbol: {symbol}")
st.markdown(f"**Current Price:** `{current_price}`")
st.markdown(f"**Nearest Round Number:** `{round_number_zone}`")
st.markdown(f"**VWAP:** `{round(vwap_value, 2)}`")
st.markdown(f"**MACD Signal:** `{macd_signal}`")

# --- HEATMAP ---
st.markdown("### 📊 MACD/VWAP Signal Heatmap")
heatmap_data = np.random.randn(10, 10)
fig, ax = plt.subplots(figsize=(8, 2.8))
cax = ax.imshow(heatmap_data, cmap='inferno', aspect='auto')
ax.set_xticks(range(10))
ax.set_xticklabels([f"T{i+1}" for i in range(10)])
ax.set_yticks(range(10))
ax.set_yticklabels([str(int(current_price - 10 + i)) for i in range(10)])
ax.set_xlabel("Signal Index (Time)")
ax.set_ylabel("Price Level")
ax.set_title("MACD/VWAP Signal Heatmap")
plt.colorbar(cax, ax=ax, label="Signal Strength")
st.pyplot(fig)

# --- SIGNAL LOG TABLE ---
st.markdown("### 📈 Recent Signals")
log_data = pd.DataFrame({
    "Time": pd.date_range(datetime.datetime.now() - datetime.timedelta(minutes=75), periods=5, freq="15min"),
    "Signal": ["BUY", "SELL", "BUY", "SELL", "BUY"],
    "Price": np.random.uniform(33500, 33700, 5).round(2)
})
st.table(log_data)

# --- CUSTOM BOT LOGIC CONFIG ---
st.markdown("### ⚙️ Custom Trade Trigger Rules")

macd_condition = st.selectbox("MACD must be:", ["BUY", "SELL", "NEUTRAL"])
price_condition = st.selectbox("Price must be:", ["> VWAP", "< VWAP", "= VWAP"])
manual_mode = st.checkbox("🔌 Manual Mode (Disable Auto-Trades)", value=False)

def evaluate_custom_logic(macd, price, vwap, macd_rule, price_rule):
    macd_match = (macd == macd_rule)

    if price_rule == "> VWAP":
        price_match = price > vwap
    elif price_rule == "< VWAP":
        price_match = price < vwap
    else:
        price_match = round(price, 2) == round(vwap, 2)

    return macd_match and price_match

# --- SHEETS LOGGING (always visible) ---
st.markdown("### 📄 Google Sheets Logging")
client = authenticate_gsheets_from_upload()

# --- FORCE TEST TRADE ---
if client and st.button("🧪 Force Dummy Trade"):
