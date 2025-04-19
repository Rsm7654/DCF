import streamlit as st
import pandas as pd
import yfinance as yf
import requests
import io

from dcf_valuation import run_dcf
from price_chart import show_chart
from financials import show_financials

st.set_page_config(page_title="📈 Stock Analyzer", layout="wide")
st.title("📊 Stock Analyzer App")

# --- Load Excel File from GitHub RAW URL ---
github_excel_url = "https://raw.githubusercontent.com/Rsm7654/DCF/main/Stock_list%20(1).xlsx"
ticker_symbol = None

try:
    # Download and read Excel from raw GitHub URL
    response = requests.get(github_excel_url)
    response.raise_for_status()
    file_bytes = io.BytesIO(response.content)
    df_stocks = pd.read_excel(file_bytes, engine='openpyxl')

    st.success("✅ Stock list loaded from GitHub.")
    st.subheader("📃 Available Stocks")
    st.dataframe(df_stocks)

    # --- Select Stock from Uploaded List ---
    if 'Ticker' in df_stocks.columns:
        selected_ticker = st.selectbox("🔍 Select a stock by ticker", df_stocks['Ticker'])
        ticker_symbol = selected_ticker
    elif 'Company' in df_stocks.columns:
        selected_company = st.selectbox("🔍 Select a stock by company name", df_stocks['Company'])
        try:
            search = yf.Search(selected_company)
            quotes = search.quotes
            if quotes:
                ticker_symbol = quotes[0]['symbol']
        except Exception as e:
            st.error(f"Search error: {e}")
            ticker_symbol = None
    else:
        st.warning("⚠️ No 'Ticker' or 'Company' column found in your Excel file.")

except Exception as e:
    st.error(f"Error loading Excel file: {e}")

# --- Load Data & Show Tabs ---
if ticker_symbol:
    ticker = yf.Ticker(ticker_symbol)

    tab1, tab2, tab3 = st.tabs(["💸 DCF Valuation", "📈 Price Chart", "📄 Financials"])

    with tab1:
        run_dcf(ticker)

    with tab2:
        show_chart(ticker)

    with tab3:
        show_financials(ticker, ticker_symbol)
