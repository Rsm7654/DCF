import streamlit as st
import pandas as pd

def format_financials(df):
    """Transpose, clean, and format numbers to ₹ crores."""
    df = df.T
    df.index = pd.to_datetime(df.index).year  # Show only the year (e.g., 2022)
    df = df / 1e7  # Convert to ₹ crores (assuming values in ₹)
    df = df.round(2)
    df.index.name = "Year"
    return df

def show_financials(ticker, symbol):
    st.subheader(f"📄 Financial Statements - {symbol}")

    try:
        st.write("### 🧾 Income Statement (₹ Crores)")
        income_df = ticker.financials
        if not income_df.empty:
            st.dataframe(format_financials(income_df))
        else:
            st.warning("No Income Statement data available.")

        st.write("### 💰 Balance Sheet (₹ Crores)")
        balance_df = ticker.balance_sheet
        if not balance_df.empty:
            st.dataframe(format_financials(balance_df))
        else:
            st.warning("No Balance Sheet data available.")

        st.write("### 💸 Cash Flow Statement (₹ Crores)")
        cashflow_df = ticker.cashflow
        if not cashflow_df.empty:
            st.dataframe(format_financials(cashflow_df))
        else:
            st.warning("No Cash Flow data available.")

    except Exception as e:
        st.error(f"Error loading financial data: {e}")
