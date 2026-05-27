import streamlit as st
import pandas as pd
import numpy as np

# 網頁標題
st.title("家庭資產成長模擬器")

# 側邊欄：輸入參數 (下拉選單與輸入框)
st.sidebar.header("參數設定")
initial_assets = st.sidebar.number_input("初始總資產 (元)", value=933796)
monthly_invest = st.sidebar.number_input("每月總投入金額 (元)", value=16000)
years = st.sidebar.slider("投資年限 (年)", 5, 30, 15)

# 報酬率設定
return_rate = st.sidebar.slider("預估年化報酬率 (%)", 5, 20, 10) / 100

# 運算邏輯
def calculate_growth(initial, monthly, rate, years):
    data = []
    current_val = initial
    for year in range(1, years + 1):
        # 加上年度投入
        invest_this_year = monthly * 12
        # 計算收益 (簡單複利模型：假設年初投入)
        earnings = (current_val + invest_this_year) * rate
        year_end_val = current_val + invest_this_year + earnings
        
        data.append({
            "年度": year,
            "期初資產": int(current_val),
            "年度投入": invest_this_year,
            "預估收益": int(earnings),
            "年末總市值": int(year_end_val)
        })
        current_val = year_end_val
    return pd.DataFrame(data)

# 顯示結果
df = calculate_growth(initial_assets, monthly_invest, return_rate, years)
st.write(f"預估未來 {years} 年的資產成長狀況：")
st.dataframe(df.style.format("{:,}"), use_container_width=True)

# 繪製圖表
st.line_chart(df.set_index("年度")["年末總市值"])