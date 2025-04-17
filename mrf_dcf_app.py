import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd

st.set_page_config(page_title="Stock Analyzer", layout="wide")

st.title("📈 Stock Analysis App")

# --- Sidebar: Feature Selection ---
feature = st.sidebar.selectbox(
    "Select Feature",
    ["📊 DCF Valuation", "📈 Price Chart", "📄 Financials"]
)

# --- Search for Company ---
company_query = st.text_input("🔍 Search Company")

ticker_symbol = None
if company_query:
    try:
        search = yf.Search(company_query)
        quotes = search.quotes
        if quotes:
            options = [f"{q['shortname']} ({q['symbol']})" for q in quotes if 'shortname' in q]
            selection = st.selectbox("Select Company", options)
            ticker_symbol = selection.split('(')[-1].strip(')')
    except Exception as e:
        st.error(f"Search error: {e}")

# --- Load ticker data ---
if ticker_symbol:
    ticker = yf.Ticker(ticker_symbol)

    if feature == "📊 DCF Valuation":
        # (Add DCF logic here — as you already have)

        st.subheader("💸 Valuation Coming Soon!")

    elif feature == "📈 Price Chart":
        st.subheader(f"📈 Stock Price Chart - {ticker_symbol}")
        hist = ticker.history(period="5y")
        st.line_chart(hist["Close"])

    elif feature == "📄 Financials":
        st.subheader(f"📄 Financial Statements - {ticker_symbol}")
        st.write("**Income Statement**")
        st.dataframe(ticker.financials.T)

        st.write("**Balance Sheet**")
        st.dataframe(ticker.balance_sheet.T)

        st.write("**Cash Flow**")
        st.dataframe(ticker.cashflow.T)
