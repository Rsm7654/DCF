import streamlit as st

def show_chart(ticker, symbol):
    st.subheader(f"📈 Stock Price Chart - {symbol}")
    hist = ticker.history(period="5y")
    st.line_chart(hist["Close"])
