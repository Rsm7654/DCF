# app.py
import streamlit as st
from dcf_valuation import run_dcf
from price_chart import run_price_chart
from financials import run_financials

st.set_page_config(page_title="📈 Stock Analyzer", layout="wide")
st.title("📊 Stock Analyzer App")

# --- Company Search ---
company_query = st.text_input("🔍 Search Company")

ticker_symbol = None
if company_query:
    try:
        import yfinance as yf
        search = yf.Search(company_query)
        quotes = search.quotes
        if quotes:
            options = [f"{q['shortname']} ({q['symbol']})" for q in quotes if 'shortname' in q]
            selection = st.selectbox("Select Company", options)
            ticker_symbol = selection.split('(')[-1].strip(')')
    except Exception as e:
        st.error(f"Search error: {e}")

# --- Load Tabs if Company Selected ---
if ticker_symbol:
    tab1, tab2, tab3 = st.tabs(["💸 DCF Valuation", "📈 Price Chart", "📄 Financials"])

    with tab1:
        run_dcf(ticker_symbol)

    with tab2:
        run_price_chart(ticker_symbol)

    with tab3:
        run_financials(ticker_symbol)
