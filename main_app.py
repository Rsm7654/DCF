import streamlit as st
import pandas as pd
import yfinance as yf
import requests
import io

from dcf_valuation import run_dcf
from price_chart import show_chart
from financials import show_financials
from peer_comparison import peer_comparison

st.set_page_config(page_title="📈 Stock Analyzer", layout="wide")
st.title("📊 Stock Analyzer App")

# --- Load Excel File from GitHub ---
github_excel_url = "https://raw.githubusercontent.com/Rsm7654/DCF/main/Stock_list%20(1).xlsx"
ticker_symbol = None
has_sector_column = False  # Track if 'Sector' exists

try:
    # Fetch and read the Excel file
    response = requests.get(github_excel_url)
    response.raise_for_status()
    file_bytes = io.BytesIO(response.content)
    df_stocks = pd.read_excel(file_bytes, engine='openpyxl')

    # Clean and validate columns
    df_stocks.columns = df_stocks.columns.str.strip()
    has_sector_column = "Sector" in df_stocks.columns

    if not {"Ticker", "Company"}.issubset(df_stocks.columns):
        st.error("❌ The Excel must contain at least 'Ticker' and 'Company' columns.")
    else:
        if not has_sector_column:
            st.warning("⚠️ 'Sector' column missing. Peer comparison will be disabled.")

        st.success("✅ Stock list loaded successfully.")

        # Build searchable dropdown
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
    st.error(f"❌ Error loading stock list: {e}")

# --- Load Ticker & Display Tabs ---
if ticker_symbol:
    ticker = yf.Ticker(ticker_symbol)

    if has_sector_column:
        tab1, tab2, tab3, tab4 = st.tabs([
            "🔗 Peer Comparison", "💸 DCF Valuation", "📈 Price Chart", "📄 Financials"
        ])

        with tab1:
            peer_comparison(ticker_symbol, df_stocks)

        with tab2:
            run_dcf(ticker)

        with tab3:
            show_chart(ticker)

        with tab4:
            show_financials(ticker, ticker_symbol)

    else:
        tab1, tab2, tab3 = st.tabs([
            "💸 DCF Valuation", "📈 Price Chart", "📄 Financials"
        ])

        with tab1:
            run_dcf(ticker)

        with tab2:
            show_chart(ticker)

        with tab3:
            show_financials(ticker, ticker_symbol)
