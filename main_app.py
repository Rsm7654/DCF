import streamlit as st
import yfinance as yf

# --- Company Search ---
company_query = st.text_input("🔍 Search Company", key="search_box")

ticker_symbol = None

if company_query:
    try:
        # Use yfinance search function
        search = yf.search(company_query)
        quotes = search['quotes']  # Adjusting for the correct API structure
        
        if quotes:
            # Prepare list of company names and ticker symbols with additional info
            options = [
                f"{q['shortname']} ({q['symbol']}) - {q.get('sector', 'N/A')} - Market Cap: {q.get('marketCap', 'N/A')}"
                for q in quotes if 'shortname' in q
            ]
            
            # Show a selectbox for company selection
            selection = st.selectbox("Select Company", options)
            ticker_symbol = selection.split('(')[-1].strip(')')

    except Exception as e:
        st.error(f"Search error: {e}")

# Proceed with loading data and showing tabs
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
