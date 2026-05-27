import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time

# =========================
# Page Config (頁面設定)
# =========================
st.set_page_config(
    page_title="AI Portfolio Pro", 
    page_icon="🧠📊", 
    layout="wide"
)

st.title("🧠📊 專業投資終極版 AI Portfolio Pro")
st.caption("量化投資｜資產配置｜風險分析｜再平衡｜投資決策輔助系統")

# =========================
# Session State Init (安全資料初始化)
# =========================
# 導入金融級 Unique ID 機制，避免動態刪除時元件 Index 移位造成 Crash
if "assets" not in st.session_state:
    st.session_state.assets = [
        {"id": "asset_init_1", "symbol": "VOO", "weight": 40.0, "return": 10.0, "risk": 15.0},
        {"id": "asset_init_2", "symbol": "QQQ", "weight": 30.0, "return": 12.0, "risk": 20.0},
        {"id": "asset_init_3", "symbol": "VTI", "weight": 30.0, "return": 8.0, "risk": 12.0},
    ]

# =========================
# Sidebar Settings (側邊欄參數)
# =========================
st.sidebar.header("⚙️ 基礎設定")
initial_assets = st.sidebar.number_input("初始資產 ($)", min_value=0, max_value=100000000, value=1000000, step=50000)
monthly_invest = st.sidebar.number_input("每月投入 ($)", min_value=0, max_value=1000000, value=20000, step=1000)
years = st.sidebar.slider("模擬年數", min_value=1, max_value=40, value=20)

st.sidebar.markdown("---")
st.sidebar.caption("AI Portfolio Pro v3 - Stable Quant Edition")

# =========================
# Asset Management CRUD (動態資產管理系統)
# =========================
st.header("🗂️ 資產配置面板")

# 1. 新增資產區塊 (使用 Form 容器防止輸入時頻繁觸發系統重繪)
with st.expander("➕ 新增自訂資產 / ETF 標的"):
    with st.form("add_asset_form", clear_on_submit=True):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            new_symbol = st.text_input("資產代號 (例如: TSLA, BND)", value="").upper().strip()
        with col2:
            new_weight = st.number_input("預設權重 (%)", min_value=0.0, max_value=100.0, value=10.0, step=5.0)
        with col3:
            new_return = st.number_input("預期年化報酬 (%)", min_value=-50.0, max_value=100.0, value=8.0, step=0.5)
        with col4:
            new_risk = st.number_input("預期波動度/風險 (%)", min_value=0.0, max_value=100.0, value=15.0, step=0.5)
        
        submit_btn = st.form_submit_button(label="直接加入資產組合")
        
        if submit_btn:
            if new_symbol:
                # 建立絕對不重複的唯一識別碼
                unique_id = f"asset_{int(time.time() * 1000)}"
                st.session_state.assets.append({
                    "id": unique_id,
                    "symbol": new_symbol,
                    "weight": new_weight,
                    "return": new_return,
                    "risk": new_risk
                })
                st.rerun()
            else:
                st.warning("請先輸入正確的資產代號。")

# 2. 顯示與動態修改編輯區
if len(st.session_state.assets) == 0:
    st.info("目前資產組合中沒有標的，請展開上方區塊新增資產。")
    st.stop()

st.subheader("資產權重即時校正")
total_input_weight = 0.0

# 安全複製一份當前資料進行渲染與就地更新
for i, asset in enumerate(st.session_state.assets):
    a_id = asset["id"]
    c1, c2, c3, c4, c5 = st.columns([2, 2, 2, 2, 1])
    
    with c1:
        asset["symbol"] = st.text_input("代號", value=asset["symbol"], key=f"sym_{a_id}").upper().strip()
    with c2:
        asset["weight"] = st.number_input("權重 (%)", min_value=0.0, max_value=100.0, value=float(asset["weight"]), key=f"w_{a_id}")
    with c3:
        asset["return"] = st.number_input("預期報酬 (%)", min_value=-50.0, max_value=100.0, value=float(asset["return"]), key=f"r_{a_id}")
    with c4:
        asset["risk"] = st.number_input("風險波動 (%)", min_value=0.0, max_value=100.0, value=float(asset["risk"]), key=f"k_{a_id}")
    with c5:
        st.write("") # 垂直對齊優化
        st.write("")
        if st.button("❌", key=f"del_{a_id}"):
            st.session_state.assets.pop(i)
            st.rerun()
            
    total_input_weight += asset["weight"]

# =========================
# Quant Calculations & Normalization (量化核心歸一化)
# =========================
df_assets = pd.DataFrame(st.session_state.assets)

if total_input_weight == 0:
    st.error("🚨 總配置權重不能為 0%，請至少為一項資產分配權重。")
    st.stop()

# 核心防禦性：自動進行權重歸一化 (Normalization)，保證系統不因權重非100而中斷
df_assets["normalized_weight"] = df_assets["weight"] / total_input_weight

# 計算資產組合綜合指標
portfolio_return = (df_assets["normalized_weight"] * (df_assets["return"] / 100)).sum()
portfolio_risk = (df_assets["normalized_weight"] * (df_assets["risk"] / 100)).sum()
sharpe_ratio = portfolio_return / portfolio_risk if portfolio_risk > 0 else 0.0

# 權重未滿 100% 時呈現平滑提示而非錯誤
if abs(total_input_weight - 100.0) > 0.01:
    st.warning(f"⚠️ 當前設定總權重為 {total_input_weight:.1f}%。系統已自動「等比例歸一化」至 100% 進行後續精確計算。")

# =========================
# Dashboard KPIs & Charts (視覺化數據面板)
# =========================
st.markdown("---")
st.header("📊 投資組合量化指標")

kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("預期年化報酬率 (Portfolio Return)", f"{portfolio_return * 100:.2f}%")
kpi2.metric("投資組合綜合風險 (Portfolio Risk)", f"{portfolio_risk * 100:.2f}%")
kpi3.metric("索提諾/夏普參考值 (Sharpe Proxy)", f"{sharpe_ratio:.2f}")

chart_col1, chart_col2 = st.columns(2)
with chart_col1:
    fig_pie = px.pie(
        df_assets, 
        values="weight", 
        names="symbol", 
        title="💼 實際資產權重配置分佈", 
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with chart_col2:
    fig_bar = px.bar(
        df_assets, 
        x="symbol", 
        y="risk", 
        title="⚠️ 各單一資產風險結構比較",
        labels={"risk": "波動度 (%)", "symbol": "資產代號"},
        color="symbol",
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# =========================
# Financial Simulation Engine (複利與動態增資模擬)
# =========================
st.markdown("---")
st.header("📈 預期複利成長軌跡預測")

# 精確到月份的複利增資演算法
total_months = years * 12
monthly_return_rate = (1 + portfolio_return) ** (1 / 12) - 1

sim_data = []
current_balance = initial_assets

for month in range(total_months + 1):
    if month > 0:
        current_balance = current_balance * (1 + monthly_return_rate) + monthly_invest
    
    sim_data.append({
        "時間 (年)": month / 12,
        "資產規模 ($)": round(current_balance, 2)
    })

df_sim = pd.DataFrame(sim_data)

# 繪製高階資產增長曲線
fig_trend = px.line(
    df_sim, 
    x="時間 (年)", 
    y="資產規模 ($)", 
    title=f"🚀 未來 {years} 年資產長期增長趨勢曲線 (結合每月定額定投)"
)
fig_trend.update_traces(line_color="#1f77b4", line_width=3)
st.plotly_chart(fig_trend, use_container_width=True)

# 詳細數據展開區
with st.expander("📋 檢視詳細年度結算數據表格"):
    # 每 12 個月切片一次，呈現清晰的年度報告
    annual_report = df_sim.iloc[::12, :].copy().reset_index(drop=True)
    annual_report["時間 (年)"] = annual_report["時間 (年)"].astype(int)
    annual_report.columns = ["結算年度", "當期資產總評估價值 ($)"]
    st.dataframe(annual_report, use_container_width=True)
