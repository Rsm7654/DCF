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

# --- Load Excel File from GitHub ---
github_excel_url = "https://raw.githubusercontent.com/Rsm7654/DCF/main/Stock_list%20(1).xlsx"
ticker_symbol = None

try:
    # Download Excel from GitHub
    response = requests.get(github_excel_url)
    response.raise_for_status()
    file_bytes = io.BytesIO(response.content)
    df_stocks = pd.read_excel(file_bytes, engine='openpyxl')


    # --- Search box ---
    company_query = st.text_input("🔍 Search Company or Ticker", "").lower()

    # --- Filter stock list ---
    if company_query:
        filtered_df = df_stocks[df_stocks.apply(
            lambda row: company_query in str(row.get('Company', '')).lower() or company_query in str(row.get('Ticker', '')).lower(), axis=1
        )]

        if not filtered_df.empty:
            # Combine company and ticker for display
            options = filtered_df.apply(lambda row: f"{row['Company']} ({row['Ticker']})", axis=1)
            selected = st.selectbox("Select Company", options)

            # Extract ticker
            ticker_symbol = selected.split('(')[-1].strip(')')
        else:
            st.warning("No matching company/ticker found.")

except Exception as e:
    st.error(f"Error loading stock list: {e}")

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
