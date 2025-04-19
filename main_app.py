import streamlit as st
import pandas as pd
import yfinance as yf
from dcf_valuation import run_dcf
from price_chart import show_chart
from financials import show_financials

st.set_page_config(page_title="📈 Stock Analyzer", layout="wide")
st.title("📊 Stock Analyzer App")

# --- Upload Stock List ---
uploaded_file = st.file_uploader("📁 Upload Stock List (CSV with 'Company' or 'Ticker' column)", type="csv")

ticker_symbol = None

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Check which column is available
    if 'Ticker' in df.columns:
        selected = st.selectbox("Select Company", df['Ticker'])
        ticker_symbol = selected
    elif 'Company' in df.columns:
        selected = st.selectbox("Select Company", df['Company'])
        
        # Optional: map company name to ticker using yfinance
        try:
            search = yf.Search(selected)
            quotes = search.quotes
            if quotes:
                ticker_symbol = quotes[0]['symbol']
        except Exception as e:
            st.error(f"Error fetching ticker: {e}")
    else:
        st.warning("Please upload a CSV with either 'Company' or 'Ticker' column.")

else:
    # --- Manual Company Search ---
    company_query = st.text_input("🔍 Or Search Company")

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
