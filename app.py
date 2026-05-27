import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
from datetime import datetime

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="Portfolio Pro Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 專業資產配置系統 Portfolio Pro")
st.caption("ETF / 股票｜動態配置｜即時價格｜資產模擬｜專業投資儀表板")

# =========================
# Session State（避免重複 key + 支援動態新增刪除）
# =========================
if "assets" not in st.session_state:
    st.session_state.assets = [
        {"symbol": "VOO", "weight": 40, "return": 10},
        {"symbol": "QQQ", "weight": 30, "return": 12},
        {"symbol": "VTI", "weight": 30, "return": 8}
    ]

# =========================
# Sidebar - 基本參數
# =========================
st.sidebar.header("⚙️ 基礎設定")

initial_assets = st.sidebar.number_input(
    "初始資產 (元)",
    0, 100000000, 1000000,
    key="init"
)

monthly_invest = st.sidebar.number_input(
    "每月投入 (元)",
    0, 1000000, 20000,
    key="monthly"
)

years = st.sidebar.slider(
    "投資年限",
    1, 40, 20,
    key="years"
)

# =========================
# Add Asset
# =========================
st.sidebar.header("➕ 新增資產")

new_symbol = st.sidebar.text_input("股票 / ETF 代號", key="new_symbol").upper()
new_weight = st.sidebar.slider("配置 (%)", 0, 100, 10, key="new_weight")
new_return = st.sidebar.slider("預估年化 (%)", 0, 30, 10, key="new_return")

if st.sidebar.button("新增資產"):
    if new_symbol:
        st.session_state.assets.append({
            "symbol": new_symbol,
            "weight": new_weight,
            "return": new_return
        })
        st.success(f"已新增 {new_symbol}")

# =========================
# 資產管理（可刪除）
# =========================
st.subheader("📌 資產配置管理")

updated_assets = []

for i, a in enumerate(st.session_state.assets):
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])

    with col1:
        symbol = st.text_input("代號", a["symbol"], key=f"s_{i}")

    with col2:
        weight = st.slider("權重", 0, 100, a["weight"], key=f"w_{i}")
st.dataframe(result, use_container_width=True)
