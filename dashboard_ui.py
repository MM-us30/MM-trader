from dashboard_ui import show_performance_panel

import streamlit as st
from performance import calculate_performance
from risk_manager import get_daily_loss, should_pause_trading

def show_performance_panel():
    perf = calculate_performance()
    daily_loss = get_daily_loss()
    pause_flag = should_pause_trading()

    st.markdown("### 📊 Strategy Performance Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Trades", perf["total_trades"])
    col2.metric("Win Rate", f"{perf['win_rate']}%")
    col3.metric("Net PnL", f"${perf['net_pnl']}")

    st.markdown("### ⚠️ Risk Monitor")
    col4, col5 = st.columns(2)
    col4.metric("Today's PnL", f"${round(daily_loss, 2)}")
    col5.metric("Auto Pause", "YES" if pause_flag else "NO")

    if pause_flag:
        st.warning("🚨 Daily loss limit hit! Trading should be paused.")
show_performance_panel()
