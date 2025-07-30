import streamlit as st
import pandas as pd

def format_financials(df):
    """Reformat financials: rows = items, columns = years in ₹ Crores."""
    df = df / 1e7  # Convert from ₹ to ₹ Crores
    df = df.round(2)
    df = df.fillna(0)
    df.columns = pd.to_datetime(df.columns).year
    df.index.name = "Line Item"
    return df

def show_financials(ticker, symbol):
    st.subheader(f"📄 Financial Statements - {symbol}")

    try:
        # Tabs for Income, Balance Sheet, Cash Flow, Ratios
        tab1, tab2, tab3, tab4 = st.tabs(["🧾 Income Statement", "💰 Balance Sheet", "💸 Cash Flow", "📊 Ratios"])

        with tab1:
            st.subheader("🧾 Income Statement")
            income = ticker.financials
            if not income.empty:
                income_df = format_financials(income)
                st.dataframe(income_df)
            else:
                st.warning("No Income Statement data found.")

        with tab2:
            st.subheader("💰 Balance Sheet")
            balance = ticker.balance_sheet
            if not balance.empty:
                balance_df = format_financials(balance)
                st.dataframe(balance_df)
            else:
                st.warning("No Balance Sheet data found.")

        with tab3:
            st.subheader("💸 Cash Flows")
            cashflow = ticker.cashflow
            if not cashflow.empty:
                st.write("📌 Available Cash Flow Line Items:", list(cashflow.index))
                cashflow_df = format_financials(cashflow)
                st.dataframe(cashflow_df)
            else:
                st.warning("No Cash Flow Statement data found.")

        with tab4:
            st.subheader("📊 Key Financial Ratios")

            # Use formatted income and balance sheet
            if not income.empty and not balance.empty:
                try:
                    income_df = format_financials(income)
                    balance_df = format_financials(balance)

                    years = income_df.columns.intersection(balance_df.columns)

                    # Extract values (safely)
                    revenue = income_df.loc["Total Revenue"] if "Total Revenue" in income_df.index else None
                    net_income = income_df.loc["Net Income"] if "Net Income" in income_df.index else None
                    total_assets = balance_df.loc["Total Assets"] if "Total Assets" in balance_df.index else None
                    total_liabilities = balance_df.loc["Total Liab"] if "Total Liab" in balance_df.index else None
                    total_equity = balance_df.loc["Total Stockholder Equity"] if "Total Stockholder Equity" in balance_df.index else None

                    if all([revenue is not None, net_income is not None, total_assets is not None, total_equity is not None]):
                        ratios = pd.DataFrame(index=years)

                        ratios["Net Profit Margin (%)"] = (net_income[years] / revenue[years]) * 100
                        ratios["Return on Assets (%)"] = (net_income[years] / total_assets[years]) * 100
                        ratios["Return on Equity (%)"] = (net_income[years] / total_equity[years]) * 100
                        if total_liabilities is not None:
                            ratios["Debt to Equity"] = (total_liabilities[years] / total_equity[years])
                        else:
                            ratios["Debt to Equity"] = None

                        ratios = ratios.round(2)
                        st.dataframe(ratios)
                    else:
                        st.warning("Some key values are missing to compute ratios.")
                except Exception as e:
                    st.error(f"Error calculating ratios: {e}")
            else:
                st.warning("Income Statement or Balance Sheet not available.")

    except Exception as e:
        st.error(f"Error loading financial statements: {e}")
