import streamlit as st
import pandas as pd
import yfinance as yf
import requests
import io

from dcf_valuation import run_dcf
from price_chart import show_chart
from financials import show_financials
from peer_comparison import Peer-to-peer Comparison

st.set_page_config(page_title="📈 Stock Analyzer", layout="wide")
st.title("📊 Stock Analyzer App")

# --- Load Excel File from GitHub ---
github_excel_url = "https://raw.githubusercontent.com/Rsm7654/DCF/main/Stock_list%20(1).xlsx"
ticker_symbol = None

try:
    # Download and read Excel
    response = requests.get(github_excel_url)
    response.raise_for_status()
    file_bytes = io.BytesIO(response.content)
    df_stocks = pd.read_excel(file_bytes, engine='openpyxl')

    st.success("✅ Stock list loaded.")

    # --- Build dropdown options
    df_stocks["SearchDisplay"] = df_stocks["Company"] + " (" + df_stocks["Ticker"] + ")"
    search_selection = st.selectbox(
        "🔍 Search and Select Company",
        df_stocks["SearchDisplay"].tolist(),
        index=None,
        placeholder="Type to search...",
    )

    if search_selection:
        ticker_symbol = search_selection.split("(")[-1].strip(")")

except Exception as e:
    st.error(f"Error loading stock list: {e}")

# --- Load Data & Show Tabs ---
if ticker_symbol:
    ticker = yf.Ticker(ticker_symbol)

    tab1, tab2, tab3, tab4 = st.tabs(["Peer-to-peer Comparison", "💸 DCF Valuation", "📈 Price Chart", "📄 Financials"])

    with tab1:
        peer comparison(ticker)
    with tab2:
        run_dcf(ticker)

    with tab3:
        show_chart(ticker)

    with tab4:
        show_financials(ticker, ticker_symbol)
   
