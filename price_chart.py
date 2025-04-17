import streamlit as st
import yfinance as yf
import pandas as pd

def show_chart(stock_name):
    st.subheader(f"📈 Stock Price Chart - {stock_name}")

    # Get 1 month data
    ticker = yf.Ticker(stock_name)
    hist = ticker.history(period="1mo")

    # Calculate price change
    price_change = hist["Close"][-1] - hist["Close"][0]
    pct_change = (price_change / hist["Close"][0]) * 100

    st.metric(label="Price", value=f"₹{hist['Close'][-1]:.2f}", delta=f"{price_change:.2f} ({pct_change:.2f}%)")

    # Line chart
    st.line_chart(hist["Close"])
