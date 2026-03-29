import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
st.set_page_config(page_title="Stock Dashboard", layout="wide")

st.title("📈 Stock Market Analysis Dashboard")
st.markdown("### 🚀 Analyze stock trends, volatility, and performance easily")

stock = st.sidebar.selectbox("Select Stock", ["AAPL", "TSLA", "GOOGL"])
start_date = st.sidebar.date_input("Start Date", datetime.date(2022, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime.date(2024, 1, 1))

data = yf.download(stock, start=start_date, end=end_date)

if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

if data.empty:
    st.error("No data found. Try different dates.")
    st.stop()

if 'Close' not in data.columns:
    st.error("Data loading issue.")
    st.stop()

st.subheader("📌 Key Summary")

latest_price = data['Close'].iloc[-1]
avg_price = data['Close'].mean()

col1, col2 = st.columns(2)
col1.metric("Latest Price", f"${latest_price:.2f}")
col2.metric("Average Price", f"${avg_price:.2f}")

st.subheader("📊 Closing Price")
st.line_chart(data['Close'])

data['MA50'] = data['Close'].rolling(50).mean()
data['MA200'] = data['Close'].rolling(200).mean()

st.subheader("📈 Moving Averages")
st.line_chart(data[['Close', 'MA50', 'MA200']])

data['Returns'] = data['Close'].pct_change()

st.subheader("📉 Daily Returns")
st.line_chart(data['Returns'])

st.subheader("📊 Insight")

volatility = data['Returns'].std()

if volatility > 0.02:
    st.warning("High volatility → High risk ⚠️")
else:
    st.success("Low volatility → Stable stock ✅")

if 'Volume' in data.columns:
    st.subheader("📊 Volume")
    st.line_chart(data['Volume'])

st.success("🚀 Dashboard Loaded Successfully")
