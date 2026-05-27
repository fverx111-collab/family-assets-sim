import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
from datetime import datetime

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="AI Portfolio Pro",
    page_icon="🧠📊",
    layout="wide"
)

st.title("🧠📊 專業投資終極版 AI Portfolio Pro")
st.caption("量化投資｜資產配置｜風險分析｜再平衡｜投資決策輔助系統")

# =========================
# Session State Init
# =========================
if "assets" not in st.session_state:
    st.session_state.assets = [
        {"symbol": "VOO", "weight": 40, "return": 10, "risk": 15},
        {"symbol": "QQQ", "weight": 30, "return": 12, "risk": 20},
        {"symbol": "VTI", "weight": 30, "return": 8, "risk": 12},
    ]

# =========================
# Sidebar Settings
# =========================
st.sidebar.header("⚙️ 基礎設定")

initial_assets = st.sidebar.number_input("初始資產", 0, 100000000, 1000000, key="init")
monthly_invest = st.sidebar.number_input("每月投入", 0, 1000000, 20000, key="monthly")
st.caption("AI Portfolio Pro v3 - Stable Quant Edition")
