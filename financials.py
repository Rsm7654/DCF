import streamlit as st
import pandas as pd

def format_financials(df):
    """Reformat financials: rows = items, columns = years in ₹ Crores."""
    df = df / 1e7  # Convert from ₹ to ₹ Crores
    df = df.round(2)
    df = df.fillna(0)
    df.columns = pd.to_datetime(df.columns).year  # Show only fiscal year
    df.index.name = "Line Item"
    return df

def show_financials(ticker, symbol):
    st.subheader(f"📄 Financial Statements - {symbol}")

    try:
        # Create tabs
        tab1, tab2, tab3 = st.tabs(["🧾 Income Statement", "💰 Balance Sheet", "💸 Cash Flow"])

        with tab1:
            income = ticker.financials
            if not income.empty:
                income_df = format_financials(income)
                st.dataframe(income_df)
            else:
                st.warning("No Income Statement data found.")

        with tab2:
            balance = ticker.balance_sheet
            if not balance.empty:
                balance_df = format_financials(balance)
                st.dataframe(balance_df)
            else:
                st.warning("No Balance Sheet data found.")

        with tab3:
            cashflow = ticker.cashflow
            if not cashflow.empty:
                cashflow_df = format_financials(cashflow)
                st.dataframe(cashflow_df)
            else:
                st.warning("No Cash Flow data found.")

    except Exception as e:
        st.error(f"Error loading financial statements: {e}")
