import yfinance as yf
import streamlit as st

# --- Company Search ---

company_query = st.text_input("🔍 Search Company", key="company_search")

ticker_symbol = None

if company_query:
    try:
        # Fetch top search results using yfinance or an external API
        search_results = yf.Ticker(company_query).info.get('longName', None)

        if search_results:
            st.write(f"Showing results for: {search_results}")
            ticker_symbol = company_query
        else:
            st.write("No results found. Try a more specific query.")
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
