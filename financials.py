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
                # Debug: Show all items available
                st.write("📌 Available Cash Flow Line Items:", list(cashflow.index))
                cashflow_df = format_financials(cashflow)
                st.dataframe(cashflow_df)
            else:
                st.warning("No Cash Flow Statement data found.")

        with tab4:
            st.subheader("📊 Key Financial Ratios")

            # Make sure we have all 3 statements
            if not income.empty and not balance.empty:
                try:
                    # Common years
                    years = income.columns.intersection(balance.columns)

                    # Extract values
                    revenue = income.loc["Total Revenue"] if "Total Revenue" in income.index else None
                    net_income = income.loc["Net Income"] if "Net Income" in income.index else None
                    total_assets = balance.loc["Total Assets"] if "Total Assets" in balance.index else None
                    total_liabilities = balance.loc["Total Liab"] if "Total Liab" in balance.index else None
                    total_equity = balance.loc["Total Stockholder Equity"] if "Total Stockholder Equity" in balance.index else None

                    if all([revenue is not None, net_income is not None, total_assets is not None, total_equity is not None]):
                        ratios = pd.DataFrame(index=years)

                        ratios["Net Profit Margin (%)"] = (net_income[years] / revenue[years]) * 100
                        ratios["Return on Assets (%)"] = (net_income[years] / total_assets[years]) * 100
                        ratios["Return on Equity (%)"] = (net_income[years] / total_equity[years]) * 100
                        ratios["Debt to Equity"] = (total_liabilities[years] / total_equity[years])

                        ratios = ratios.round(2)
                        st.dataframe(ratios)
                    else:
                        st.warning("Some values are missing to compute ratios.")
                except Exception as e:
                    st.error(f"Error calculating ratios: {e}")
            else:
                st.warning("Income Statement or Balance Sheet not available.")

    except Exception as e:
        st.error(f"Error loading financial statements: {e}")
