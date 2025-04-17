import streamlit as st
import yfinance as yf

# Function to get suggestions based on the search query
def get_suggestions(company_query):
    """Fetch company suggestions from Yahoo Finance based on the input query."""
    try:
        search = yf.search(company_query)
        quotes = search['quotes']
        return [f"{q['shortname']} ({q['symbol']})" for q in quotes if 'shortname' in q]
    except Exception as e:
        st.error(f"Error fetching suggestions: {e}")
        return []

st.set_page_config(page_title="📈 Stock Analyzer", layout="wide")
st.title("📊 Stock Analyzer App")

# --- Company Search with Suggestions ---
company_query = st.text_input("🔍 Search Company")

if company_query:
    # Get company suggestions based on the query
    suggestions = get_suggestions(company_query)
    
    if suggestions:
        selection = st.selectbox("Select a Company", suggestions)
        ticker_symbol = selection.split('(')[-1].strip(')')
    else:
        st.warning("No suggestions found.")
        ticker_symbol = None
else:
    ticker_symbol = None

# --- Load Data & Show Tabs ---
if ticker_symbol:
    ticker = yf.Ticker(ticker_symbol)

    tab1, tab2, tab3 = st.tabs(["💸 DCF Valuation", "📈 Price Chart", "📄 Financials"])

    # --- DCF Valuation --- 
    with tab1:
        # Add your DCF Valuation code here
        st.write("💸 DCF Valuation placeholder")

    # --- Price Chart --- 
    with tab2:
        # Add your Price Chart code here
        st.write("📈 Price Chart placeholder")

    # --- Financials --- 
    with tab3:
        # Add your Financials code here
        st.write("📄 Financials placeholder")

