import streamlit as st
import pandas as pd

def format_financials(df):
    """Reformat financials: rows = items, columns = years in ₹ Crores."""
    df = df / 1e7  # ₹ to ₹ Crores
    df = df.round(2)
    df = df.fillna(0)
    df.columns = pd.to_datetime(df.columns).year
    df.index.name = "Line Item"
    return df

def safe_get(df, row_name):
    """Safely get a row from a DataFrame, returns None if not found."""
    return df.loc[row_name] if row_name in df.index else None

def show_financials(ticker, symbol):
    st.subheader(f"📄 Financial Statements - {symbol}")

    try:
        tab1, tab2, tab3, tab4 = st.tabs(["🧾 Income Statement", "💰 Balance Sheet", "💸 Cash Flow", "📊 Ratios"])

        with tab1:
            st.subheader("🧾 Income Statement")
            income = ticker.financials
            if not income.empty:
                st.dataframe(format_financials(income))
            else:
                st.warning("No Income Statement data found.")

        with tab2:
            st.subheader("💰 Balance Sheet")
            balance = ticker.balance_sheet
            if not balance.empty:
                st.dataframe(format_financials(balance))
            else:
                st.warning("No Balance Sheet data found.")

        with tab3:
            st.subheader("💸 Cash Flows")
            cashflow = ticker.cashflow
            if not cashflow.empty:
                st.write("📌 Available Cash Flow Line Items:", list(cashflow.index))
                st.dataframe(format_financials(cashflow))
            else:
                st.warning("No Cash Flow Statement data found.")

        with tab4:
            st.subheader("📊 Key Financial Ratios")
            income = ticker.financials
            balance = ticker.balance_sheet

            if not income.empty and not balance.empty:
                try:
                    income_df = format_financials(income)
                    balance_df = format_financials(balance)

                    # Align years across statements
                    common_years = income_df.columns.intersection(balance_df.columns)

                    # Safely extract required rows
                    revenue = safe_get(income_df, "Total Revenue")
                    net_income = safe_get(income_df, "Net Income")
                    total_assets = safe_get(balance_df, "Total Assets")
                    total_equity = safe_get(balance_df, "Total Stockholder Equity")
                    total_liab = safe_get(balance_df, "Total Liab")
                    current_assets = safe_get(balance_df, "Total Current Assets")
                    current_liab = safe_get(balance_df, "Total Current Liabilities")

                    # Check presence of required rows
                    if all(x is not None for x in [revenue, net_income, total_assets, total_equity]):
                        ratios = pd.DataFrame(index=common_years)

                        ratios["Net Profit Margin (%)"] = (net_income[common_years] / revenue[common_years]) * 100
                        ratios["Return on Assets (%)"] = (net_income[common_years] / total_assets[common_years]) * 100
                        ratios["Return on Equity (%)"] = (net_income[common_years] / total_equity[common_years]) * 100

                        if total_liab is not None:
                            ratios["Debt to Equity"] = total_liab[common_years] / total_equity[common_years]

                        if current_assets is not None and current_liab is not None:
                            ratios["Current Ratio"] = current_assets[common_years] / current_liab[common_years]

                        ratios["Equity Ratio"] = total_equity[common_years] / total_assets[common_years]

                        st.dataframe(ratios.round(2))

                    else:
                        st.warning("Some required rows are missing to compute financial ratios.")

                except Exception as e:
                    st.error(f"Error calculating ratios: {e}")
            else:
                st.warning("Income Statement or Balance Sheet not available.")

    except Exception as e:
        st.error(f"Error loading financial statements: {e}")
