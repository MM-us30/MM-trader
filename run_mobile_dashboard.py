import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import random
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 🔐 Google Sheets authentication
def authenticate_gsheets_from_upload():
    uploaded_file = st.file_uploader("🔐 Upload your Google JSON key", type=["json"])
    if uploaded_file is not None:
        try:
            content = json.load(uploaded_file)
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
    else:
        st.info("📥 Please upload your JSON key to enable Google Sheets logging.")
    return None

# 🔢 Simulated trading data
symbol = "US30"
current_price = round(random.uniform(33500, 33700), 2)
vwap_value = current_price - random.uniform(-20, 20)
macd_signal = random.choice(["BUY", "SELL", "NEUTRAL"])
round_number_zone = round(round(current_price / 100) * 100)

# ⚙️ App config
st.set_page_config(page_title="Chameleon Dashboard", layout="centered")
st.markdown("<h1 style='text-align: center;'>🦎 Chameleon Trading Dashboard</h1>", unsafe_allow_html=True)

# 🧭 Signal overview
st.subheader(f"Symbol: {symbol}")
st.markdown(f"**Current Price:** `{current_price}`")
st.markdown(f"**Nearest Round Number:** `{round_number_zone}`")
st.markdown(f"**VWAP:** `{round(vwap_value, 2)}`")
st.markdown(f"**MACD Signal:** `{macd_signal}`")

# 🔥 Restored MACD/VWAP Signal Heatmap (classic layout)
st.markdown("### 📊 MACD/VWAP Signal Heatmap")
heatmap_data = np.random.randn(10, 10)
fig, ax = plt.subplots(figsize=(8, 2.8))
cax = ax.imshow(heatmap_data, cmap='RdYlGn', aspect='auto')

# Custom ticks to simulate time and price levels
ax.set_xticks(range(10))
ax.set_xticklabels([f"T{i+1}" for i in range(10)])
ax.set_yticks(range(10))
ax.set_yticklabels([str(int(current_price - 10 + i)) for i in range(10)])

ax.set_xlabel("Signal Index (Time)")
ax.set_ylabel("Price Level")
ax.set_title("MACD/VWAP Signal Heatmap")
plt.colorbar(cax, ax=ax, label="Signal Strength")
st.pyplot(fig)

# 📋 Recent signals
st.markdown("### 📈 Recent Signals")
log_data = pd.DataFrame({
    "Time": pd.date_range(datetime.datetime.now() - datetime.timedelta(minutes=75), periods=5, freq="15min"),
    "Signal": ["BUY", "SELL", "BUY", "SELL", "BUY"],
    "Price": np.random.uniform(33500, 33700, 5).round(2)
})
st.table(log_data)

# 🧠 Bot Controls
st.markdown("### 🤖 Bot Controls")
col1, col2 = st.columns(2)
with col1:
    st.button("▶️ Start Chameleon Bot")
with col2:
    st.button("⏸ Pause Bot")

# 💸 Position & PnL
st.markdown("### 💰 Position & PnL")
st.metric(label="Open Position", value="BUY 1.0 lot")
st.metric(label="Current PnL", value="+$124.67")

# 📤 Google Sheets Logging
st.markdown("### 📄 Google Sheets Logging")
client = authenticate_gsheets_from_upload()

if client:
    try:
        sheet = client.open("Chameleon_Trade_Logs")
        worksheet = sheet.worksheet("Live_Trades")

        row = [
            datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            "BUY",
            symbol,
            current_price,
            1.0,
            macd_signal,
            "+124.67"
        ]
        worksheet.append_row(row)
        st.success("✅ Trade logged to Google Sheet successfully.")

    except gspread.exceptions.SpreadsheetNotFound:
        st.error("❌ Spreadsheet 'Chameleon_Trade_Logs' not found. Please create it or share access with the service account.")
    except gspread.exceptions.WorksheetNotFound:
        st.error("❌ Worksheet 'Live_Trades' not found. Please ensure it exists in the spreadsheet.")
    except Exception as e:
        st.error(f"❌ Failed to log trade: {e}")

# 🧾 Footer
st.caption("🔧 Built for mobile-first control and trade confidence using the Chameleon Logic.")
