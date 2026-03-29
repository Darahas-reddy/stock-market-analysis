import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

st.set_page_config(page_title="Stock Dashboard", layout="wide")

st.title("📈 Stock Market Analysis Dashboard")
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
    st.error("Data loading issue. Try again.")
    st.stop()

st.subheader(f"{stock} Stock Data")
st.write(data.tail())
st.subheader("📊 Closing Price")
st.line_chart(data['Close'])

data['MA50'] = data['Close'].rolling(50).mean()
data['MA200'] = data['Close'].rolling(200).mean()

st.subheader("📈 Moving Averages")
st.line_chart(data[['Close', 'MA50', 'MA200']])

data['Returns'] = data['Close'].pct_change()

st.subheader("📉 Daily Returns")
st.line_chart(data['Returns'])

if 'Volume' in data.columns:
    st.subheader("📊 Volume Traded")
    st.line_chart(data['Volume'])

st.success("Dashboard Loaded Successfully 🚀")
