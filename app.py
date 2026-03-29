import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
import mplfinance as mpf

st.set_page_config(page_title="Stock Dashboard", layout="wide")

st.title("📈 Stock Market Analysis Dashboard")

stocks = st.sidebar.multiselect(
    "Select Stocks",
    ["AAPL", "TSLA", "GOOGL"],
    default=["AAPL"]
)

start_date = st.sidebar.date_input("Start Date", datetime.date(2022, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime.date(2024, 1, 1))

if not stocks:
    st.warning("Please select at least one stock")
    st.stop()

data = yf.download(stocks, start=start_date, end=end_date)

if isinstance(data.columns, pd.MultiIndex):
    data.columns = [' '.join(col).strip() for col in data.columns.values]

if data.empty:
    st.error("No data found")
    st.stop()

st.subheader("📊 Closing Price Comparison")

close_cols = [col for col in data.columns if "Close" in col]
st.line_chart(data[close_cols])

if len(stocks) == 1:
    stock = stocks[0]
    
    st.subheader("📈 Moving Averages")
    
    data[f"MA50"] = data[f"Close {stock}"].rolling(50).mean()
    data[f"MA200"] = data[f"Close {stock}"].rolling(200).mean()
    
    st.line_chart(data[[f"Close {stock}", "MA50", "MA200"]])

st.subheader("📉 Daily Returns")

returns = data[close_cols].pct_change()
st.line_chart(returns)

st.subheader("📊 Volume")

volume_cols = [col for col in data.columns if "Volume" in col]
st.line_chart(data[volume_cols])

if len(stocks) == 1:
    st.subheader("🕯 Candlestick Chart")
    
    stock = stocks[0]
    
    df = yf.download(stock, start=start_date, end=end_date)
    
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    
    fig, axlist = mpf.plot(
        df,
        type='candle',
        volume=True,
        returnfig=True
    )
    
    st.pyplot(fig)

st.subheader("📌 Latest Stats")

cols = st.columns(len(stocks))

for i, stock in enumerate(stocks):
    df = yf.download(stock, start=start_date, end=end_date)
    
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    
    if not df.empty:
        last_price = df['Close'].iloc[-1]
        change = df['Close'].pct_change().iloc[-1] * 100
        
        cols[i].metric(
            label=stock,
            value=f"${last_price:.2f}",
            delta=f"{change:.2f}%"
        )

st.success("🚀 Dashboard Loaded Successfully")
