import streamlit as st
import yfinance as yf
from dcf_valuation import run_dcf
from price_chart import show_chart
from financials import show_financials

st.set_page_config(page_title="📈 Stock Analyzer", layout="wide")
st.title("📊 Stock Analyzer App")

# --- Company Search ---
company_query = st.text_input("🔍 Search Company")

ticker_symbol = None
if company_query:
    try:
        search = yf.Search(company_query)
        quotes = search.quotes
        if quotes:
            # Filter out results without a short name (less informative)
            valid_quotes = [q for q in quotes if 'shortname' in q and 'symbol' in q]

            if not valid_quotes:
                st.warning("No relevant companies found. Please try a different search term.")
            else:
                options = [f"{q['shortname']} ({q['symbol']})" for q in valid_quotes]
                selection = st.selectbox("Select Company", options)
                ticker_symbol = selection.split('(')[-1].strip(')')
        else:
            st.warning("No companies found matching your search query.")
    except Exception as e:
        st.error(f"Search error: {e}")

# --- Load Data & Show Tabs ---
if ticker_symbol:
    ticker = yf.Ticker(ticker_symbol)

    tab1, tab2, tab3 = st.tabs(["💸 DCF Valuation", "📈 Price Chart", "📄 Financials"])

    # --- DCF Valuation ---
    with tab1:
        run_dcf(ticker)

    # --- Price Chart ---
    with tab2:
        show_chart(ticker)

    # --- Financials ---
    with tab3:
        show_financials(ticker, ticker_symbol)
