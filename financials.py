import streamlit as st

def show_financials(ticker, symbol):
    st.subheader(f"📄 Financial Statements - {symbol}")
    st.write("**Income Statement**")
    st.dataframe(ticker.financials.T)

    st.write("**Balance Sheet**")
    st.dataframe(ticker.balance_sheet.T)

    st.write("**Cash Flow**")
    st.dataframe(ticker.cashflow.T)
