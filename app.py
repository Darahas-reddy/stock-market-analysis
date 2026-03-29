import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Stock Dashboard", layout="wide")

st.title("📈 Stock Market Analysis Dashboard")

# Sidebar
stock = st.sidebar.selectbox("Select Stock", ["AAPL", "TSLA", "GOOGL"])
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2022-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2024-01-01"))

# Load Data
data = yf.download(stock, start=start_date, end=end_date)

# Show Data
st.subheader(f"{stock} Stock Data")
st.write(data.tail())

# Closing Price Chart
st.subheader("📊 Closing Price")
st.line_chart(data['Close'])

# Moving Average
data['MA50'] = data['Close'].rolling(50).mean()
data['MA200'] = data['Close'].rolling(200).mean()

st.subheader("📈 Moving Averages")
st.line_chart(data[['Close', 'MA50', 'MA200']])

# Daily Returns
data['Returns'] = data['Close'].pct_change()

st.subheader("📉 Daily Returns")
st.line_chart(data['Returns'])

st.success("Dashboard Loaded Successfully 🚀")
