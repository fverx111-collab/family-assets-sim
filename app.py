# 升級版 `app.py`（正式部署版｜多股票 ETF 資產模擬器）

```python
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

    selected = st.sidebar.selectbox(
        f"選擇 ETF / 股票 {i+1}",
        preset_options,
        key=f"preset_{i}"
    )

    if selected == "自訂輸入":
        symbol = st.sidebar.text_input(
            f"輸入代號 {i+1}",
            value="AAPL",
            key=f"custom_{i}"
        ).upper()
    else:
        symbol = selected

    allocation = st.sidebar.slider(
        f"{symbol} 配置比例 (%)",
        0,
        100,
        int(100 / asset_count),
        key=f"allocation_{i}"
    )

    default_return = 10

    annual_return = st.sidebar.slider(
        f"{symbol} 預估年化報酬率 (%)",
        0,
        30,
        default_return,
        key=f"return_{i}"
    )

    assets.append({
        "代號": symbol,
        "配置": allocation,
        "年化報酬率": annual_return / 100
    })

# =========================
# 配置檢查
# =========================
allocation_sum = sum(x["配置"] for x in assets)

if allocation_sum != 100:
    st.error(f"⚠️ 配置比例必須等於 100%，目前為 {allocation_sum}%")
    st.stop()

# =========================
# 即時股價取得
# =========================
@st.cache_data(ttl=3600)
def get_stock_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info

        current_price = info.get("currentPrice")
        previous_close = info.get("previousClose")
        long_name = info.get("longName", symbol)

        if current_price and previous_close:
            change_pct = (
                (current_price - previous_close)
                / previous_close
            ) * 100
        else:
            change_pct = 0

        return {
            "name": long_name,
            "price": current_price,
            "change": change_pct
        }

    except:
        return {
            "name": symbol,
            "price": None,
            "change": None
        }

# =========================
# 投資組合資訊
# =========================
st.subheader("📌 投資組合")

portfolio_df = pd.DataFrame(assets)

stock_infos = []

for asset in assets:
    data = get_stock_data(asset["代號"])

    stock_infos.append({
        "代號": asset["代號"],
        "名稱": data["name"],
        "配置": f'{asset["配置"]}%',
        "預估年化": f'{asset["年化報酬率"] * 100:.1f}%',
        "現價": data["price"],
        "漲跌幅": (
            f'{data["change"]:.2f}%'
            if data["change"] is not None
            else "N/A"
        )
    })

stock_df = pd.DataFrame(stock_infos)

st.dataframe(stock_df, use_container_width=True)

# =========================
# 圓餅圖
# =========================
fig = px.pie(
    portfolio_df,
    values="配置",
    names="代號",
    title="資產配置比例"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# 加權平均報酬率
# =========================
weighted_return = sum(
    x["配置"] / 100 * x["年化報酬率"]
    for x in assets
)

# =========================
# 成長模擬
# =========================
def calculate_growth(initial, monthly, annual_rate, years):

    records = []
    current_value = initial

    for year in range(1, years + 1):

        yearly_invest = monthly * 12

        earnings = (
            current_value + yearly_invest
        ) * annual_rate

        end_value = (
            current_value
            + yearly_invest
            + earnings
        )

        records.append({
            "年度": year,
            "期初資產": int(current_value),
            "年度投入": int(yearly_invest),
            "預估收益": int(earnings),
            "年末總資產": int(end_value)
        })

        current_value = end_value

    return pd.DataFrame(records)

# =========================
# 執行模擬
# =========================
df = calculate_growth(
    initial_assets,
    monthly_invest,
    weighted_return,
    years
)

# =========================
# KPI 指標
# =========================
final_assets = int(df.iloc[-1]["年末總資產"])

total_invested = int(
    initial_assets + monthly_invest * 12 * years
)

profit = final_assets - total_invested

st.subheader("📈 投資成果")

col1, col2, col3 = st.columns(3)

col1.metric(
    "最終資產",
    f"${final_assets:,}"
)

col2.metric(
    "總投入",
    f"${total_invested:,}"
)

col3.metric(
    "預估獲利",
    f"${profit:,}"
)

st.success(
    f"📊 投資組合加權年化報酬率：{weighted_return * 100:.2f}%"
)

# =========================
# 成長曲線
# =========================
st.subheader("📉 資產成長曲線")

fig2 = px.line(
    df,
    x="年度",
    y="年末總資產",
    markers=True
)

st.plotly_chart(fig2, use_container_width=True)

# =========================
# 詳細表格
# =========================
st.subheader("📋 詳細年度報表")

st.dataframe(
    df.style.format("{:,}"),
    use_container_width=True
)

# =========================
# 匯出 CSV
# =========================
csv = df.to_csv(index=False).encode("utf-8-sig")

st.download_button(
    label="📥 匯出 CSV",
    data=csv,
    file_name=f"portfolio_simulation_{datetime.now().date()}.csv",
    mime="text/csv"
)

# =========================
# Footer
# =========================
st.caption("Powered by Streamlit + Yahoo Finance")
```

---

# 你現在只需要做兩件事

## 1️⃣ requirements.txt

新增：

```txt
streamlit
pandas
yfinance
plotly
```

---

## 2️⃣ 推到 GitHub

```bash
git add .
git commit -m "upgrade portfolio simulator"
git push
```

---

# Streamlit Cloud 會自動重新部署

之後你的網站會變成：

✅ 多 ETF 管理
✅ 即時股價
✅ ETF 配置圖
✅ KPI 投資儀表板
✅ CSV 匯出
✅ 正式版 UI

---

# 下一階段還能升級

## 🔥 我建議你下一版直接做：

### 1. 股息再投入模擬

會非常實用。

---

### 2. 自動抓歷史年化報酬

不用手動輸入。

---

### 3. 美股 / 台股雙幣別

台幣、美金切換。

---

### 4. FIRE 財富自由預估

推算幾歲退休。

---

### 5. AI 投資建議

自動分析：

* 配置是否過度集中
* 風險等級
* 成長型 / 配息型

---

# 你目前這版其實已經接近：

「真正可以公開部署給別人用的投資工具」
