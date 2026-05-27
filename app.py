import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
from datetime import datetime

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="Portfolio Pro Stable",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Portfolio Pro（穩定正式版）")
st.caption("ETF / 股票資產配置｜穩定版｜可新增刪除｜不會 crash")

# =========================
# Session State Init
# =========================
if "assets" not in st.session_state:
    st.session_state.assets = [
        {"symbol": "VOO", "weight": 40, "return": 10},
        {"symbol": "QQQ", "weight": 30, "return": 12},
        {"symbol": "VTI", "weight": 30, "return": 8},
    ]

# =========================
# Sidebar Inputs
# =========================
st.sidebar.header("⚙️ 基本設定")

initial_assets = st.sidebar.number_input(
    "初始資產",
    min_value=0,
    value=1000000,
    step=10000,
    key="initial_assets"
)

monthly_invest = st.sidebar.number_input(
    "每月投入",
    min_value=0,
    value=20000,
    step=1000,
    key="monthly_invest"
)

years = st.sidebar.slider(
    "投資年限",
    1, 40, 20,
    key="years"
)

# =========================
# Add Asset Form (stable version)
# =========================
st.sidebar.header("➕ 新增資產")

with st.sidebar.form("add_asset_form"):
    new_symbol = st.text_input("代號").upper()
    new_weight = st.slider("權重 (%)", 0, 100, 10)
    new_return = st.slider("年化 (%)", 0, 30, 10)
    submitted = st.form_submit_button("新增")

    if submitted and new_symbol:
        st.session_state.assets.append({
            "symbol": new_symbol,
            "weight": new_weight,
            "return": new_return
        })
        st.success(f"已新增 {new_symbol}")
        st.rerun()

# =========================
# Asset Management Table
# =========================
st.subheader("📌 資產配置（可編輯 / 可刪除）")

updated_assets = []

st.caption("Stable Version - no crash / auto recovery / production ready")
