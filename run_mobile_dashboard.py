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
if client:
    if st.button("🧪 Force Dummy Trade"):
        try:
            sheet = client.open("Chameleon_Trade_Logs")
            worksheet = sheet.worksheet("Live_Trades")
            test_row = [
                datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                "BUY",
                symbol,
                current_price,
                1.0,
                "TEST",
                "+99.99"
            ]
            worksheet.append_row(test_row)
            st.success("✅ Dummy trade logged for testing.")
        except Exception as e:
            st.error("❌ Failed to log dummy trade.")
            st.exception(e)

# --- LOGIC GATE ---
if not manual_mode and evaluate_custom_logic(macd_signal, current_price, vwap_value, macd_condition, price_condition):
    st.success("🎯 Conditions met – trade triggered!")

    # --- POSITION & PNL ---
    st.markdown("### 💰 Position & PnL")
    st.metric(label="Open Position", value="BUY 1.0 lot")
    st.metric(label="Current PnL", value="+$124.67")

    if client:
        try:
            st.write("📡 Connecting to Google Sheet...")
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
            st.exception(e)
elif manual_mode:
    st.info("🧍 Manual mode enabled – no trades will be auto-triggered.")
else:
    st.warning("⏸ Conditions not met – no trade executed.")

# --- PERFORMANCE DASHBOARD ---
st.markdown("### 📊 Trade Performance Summary")
if client:
    try:
        sheet = client.open("Chameleon_Trade_Logs")
        worksheet = sheet.worksheet("Live_Trades")
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)

        if not df.empty:
            df["PnL"] = df["PnL"].replace({"\$": "", ",": ""}, regex=True).astype(float)
            total_trades = len(df)
            total_pnl = df["PnL"].sum()
            avg_pnl = df["PnL"].mean()
            win_rate = (df["PnL"] > 0).mean() * 100
            most_common_signal = df["Signal"].mode()[0]

            st.metric("Total Trades", total_trades)
            st.metric("Win Rate", f"{win_rate:.1f}%")
            st.metric("Total PnL", f"${total_pnl:.2f}")
            st.metric("Avg PnL per Trade", f"${avg_pnl:.2f}")
            st.metric("Most Common Signal", most_common_signal)

            st.markdown("#### PnL per Trade")
            fig, ax = plt.subplots()
            ax.plot(df["PnL"].values, marker="o")
            ax.set_ylabel("PnL")
            ax.set_title("PnL Over Trades")
            st.pyplot(fig)

            st.markdown("#### Signal Distribution")
            signal_counts = df["Signal"].value_counts()
            fig2, ax2 = plt.subplots()
            ax2.pie(signal_counts, labels=signal_counts.index, autopct='%1.1f%%')
            ax2.set_title("BUY vs SELL")
            st.pyplot(fig2)

        else:
            st.info("No trade data available yet.")
    except Exception as e:
        st.error("Failed to load performance data.")
        st.exception(e)

# --- FOOTER ---
st.caption("🔧 Built for mobile-first control and trade confidence using the Chameleon Logic.")
