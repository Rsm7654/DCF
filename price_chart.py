import streamlit as st

def show_chart(ticker):
    st.subheader(f"📈 Stock Price Chart - {ticker}")
    hist = ticker.history(period="5y")
    st.line_chart(hist["Close"])
