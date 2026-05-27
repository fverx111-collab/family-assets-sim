import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
from datetime import datetime

# =========================
# 頁面設定
# =========================
st.set_page_config(
    page_title="家庭資產成長模擬器",
    page_icon="📈",
    layout="wide"
)

# =========================
# 標題
# =========================
st.title("📈 家庭資產成長模擬器")
st.caption("多股票 / ETF 投資配置模擬｜即時股價｜資產成長分析")

# =========================
# 側邊欄
# =========================
st.sidebar.header("⚙️ 投資設定")

initial_assets = st.sidebar.number_input(
    "初始資產 (元)",
    min_value=0,
    value=933796,
    step=10000
)

monthly_invest = st.sidebar.number_input(
    "每月投入金額 (元)",
    min_value=0,
    value=16000,
    step=1000
)

years = st.sidebar.slider(
    "投資年限",
    1,
    40,
    15
)

st.sidebar.divider()

# =========================
# 股票 / ETF 設定
# =========================
st.sidebar.header("📊 股票 / ETF 配置")

asset_count = st.sidebar.number_input(
    "投資標的數量",
    min_value=1,
    max_value=10,
    value=3
)

preset_options = [
    "0050.TW",
    "006208.TW",
    "00878.TW",
    "00919.TW",
    "0056.TW",
    "VOO",
    "QQQ",
    "SPY",
    "VTI",
    "VT",
    "SCHD",
    "自訂輸入"
]

assets = []

# =========================
# 建立配置
# =========================
for i in range(asset_count):

    st.sidebar.markdown(f"### 標的 {i+1}")
st.caption("Powered by Streamlit + Yahoo Finance")
