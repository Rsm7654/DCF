import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd

# Set page config
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

# --- Tabs for each feature ---
if ticker_symbol:
    ticker = yf.Ticker(ticker_symbol)

    # Create tabs
    tabs = ["DCF Valuation", "Price Chart", "Financials"]
    tab = st.radio("Select Tab", tabs)

    if tab == "DCF Valuation":
        # DCF Valuation logic here
        st.subheader("💸 DCF Valuation")

        growth_rate = st.slider("Growth Rate (%)", 0.0, 20.0, 10.0) / 100
        terminal_growth = st.slider("Terminal Growth Rate (%)", 0.0, 10.0, 4.0) / 100
        wacc = st.slider("Discount Rate / WACC (%)", 0.0, 20.0, 10.0) / 100

        # Fetching
