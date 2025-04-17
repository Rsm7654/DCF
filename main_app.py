import streamlit as st
import yfinance as yf

st.set_page_config(page_title="📈 Stock Analyzer", layout="wide")
st.title("📊 Stock Analyzer App")

# --- State to store search results ---
if 'search_results' not in st.session_state:
    st.session_state['search_results'] = []

# --- Function to perform the search ---
def perform_search(query):
    if query:
        try:
            search = yf.Search(query)
            st.session_state['search_results'] = search.quotes
        except Exception as e:
            st.error(f"Search error: {e}")
    else:
        st.session_state['search_results'] = []

# --- Search Bar ---
company_query = st.text_input("🔍 Search Company", on_change=perform_search, args=(st.session_state.get('search_input', ""),))
st.session_state['search_input'] = company_query

# --- Display Recommendations ---
if st.session_state['search_results']:
    valid_recommendations = [
        f"{q.get('shortname', 'N/A')} ({q.get('symbol', 'N/A')})"
        for q in st.session_state['search_results']
        if q.get('shortname') and q.get('symbol')
    ]
    if valid_recommendations:
        selected_company = st.selectbox("Select Company", valid_recommendations)
        ticker_symbol = selected_company.split('(')[-1].strip(')')

        if ticker_symbol:
            st.subheader(f"Analyzing: {selected_company}")
            ticker = yf.Ticker(ticker_symbol)

            tab1, tab2, tab3 = st.tabs(["💸 DCF Valuation", "📈 Price Chart", "📄 Financials"])

            # Import your other modules here to avoid circular dependencies
            from dcf_valuation import run_dcf
            from price_chart import show_chart
            from financials import show_financials

            # --- DCF Valuation ---
            with tab1:
                run_dcf(ticker)

            # --- Price Chart ---
            with tab2:
                show_chart(ticker)

            # --- Financials ---
            with tab3:
                show_financials(ticker, ticker_symbol)
    else:
        st.warning("No relevant companies found.")
elif company_query:
    st.info("Start typing to see company recommendations.")
