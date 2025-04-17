import streamlit as st
import pandas as pd

# ---------- Helper Functions ----------

def format_financials(df):
    df = df / 1e7  # Convert from ₹ to ₹ Crores
    df = df.round(2)
    df = df.fillna(0)
    df.columns = pd.to_datetime(df.columns).year
    df.index.name = "Line Item"
    return df

def show_financials(ticker, symbol):
    st.subheader(f"📄 Financial Statements - {symbol}")

    try:
        # Create tabs for Income Statement, Balance Sheet, and Cash Flow
        tab1, tab2, tab3, tab4 = st.tabs(["🧾 Income Statement", "💰 Balance Sheet", "💸 Cash Flow", "📊 Ratios"])

        with tab1:
            income = ticker.financials
            if not income.empty:
                income_df = format_financials(income)
                show_income_statement(income_df)
            else:
                st.warning("No Income Statement data found.")

        with tab2:
            balance = ticker.balance_sheet
            if not balance.empty:
                balance_df = format_financials(balance)
                show_balance_sheet(balance_df)
            else:
                st.warning("No Balance Sheet data found.")

        with tab3:
            cashflow = ticker.cashflow
            if not cashflow.empty:
                cashflow_df = format_financials(cashflow)
                show_cashflow_statement(cashflow_df)
            else:
                st.warning("No Cash Flow data found.")

        with tab4:
            income = ticker.financials
            balance = ticker.balance_sheet
            if not income.empty and not balance.empty:
                income_df = format_financials(income)
                balance_df = format_financials(balance)
                show_financial_ratios(income_df, balance_df)
            else:
                st.warning("Not enough data to compute ratios.")

    except Exception as e:
        st.error(f"Error loading financial statements: {e}")

def show_income_statement(income_df):
    st.markdown("### 📟 Income Statement")

    line_items = [
        "Total Revenue",
        "Cost Of Revenue",
        "Gross Profit",
        "Operating Expense",
        "Operating Income",
        "Interest Expense",
        "Total Other Income/Expense Net",
        "Income Before Tax",
        "Income Tax Expense",
        "Net Income"
    ]

    existing = [item for item in line_items if item in income_df.index]
    df = income_df.loc[existing]

    df.rename(index={
        "Total Revenue": "Revenue",
        "Cost Of Revenue": "Cost of Goods Sold",
        "Gross Profit": "Gross Profit",
        "Operating Expense": "Operating Expenses",
        "Operating Income": "Operating Income (EBIT)",
        "Interest Expense": "Interest Expense",
        "Total Other Income/Expense Net": "Other Income/Expense",
        "Income Before Tax": "Earnings Before Tax (EBT)",
        "Income Tax Expense": "Income Tax",
        "Net Income": "Net Income"
    }, inplace=True)

    st.dataframe(df.style.format("{:.2f}"))

def show_balance_sheet(balance_df):
    st.markdown("### 💰 Balance Sheet")

    line_items = [
        "Cash And Cash Equivalents",
        "Short Term Investments",
        "Net Receivables",
        "Inventory",
        "Total Current Assets",
        "Property Plant And Equipment",
        "Goodwill",
        "Total Assets",
        "Accounts Payable",
        "Short Term Debt",
        "Total Current Liabilities",
        "Long Term Debt",
        "Total Liabilities",
        "Common Stock",
        "Retained Earnings",
        "Total Stockholder Equity",
        "Total Liabilities And Stockholder Equity"
    ]

    existing = [item for item in line_items if item in balance_df.index]
    df = balance_df.loc[existing]

    df.rename(index={
        "Cash And Cash Equivalents": "Cash & Equivalents",
        "Short Term Investments": "Short Term Investments",
        "Net Receivables": "Net Receivables",
        "Inventory": "Inventory",
        "Total Current Assets": "Total Current Assets",
        "Property Plant And Equipment": "PP&E",
        "Goodwill": "Goodwill",
        "Total Assets": "Total Assets",
        "Accounts Payable": "Accounts Payable",
        "Short Term Debt": "Short Term Debt",
        "Total Current Liabilities": "Total Current Liabilities",
        "Long Term Debt": "Long Term Debt",
        "Total Liabilities": "Total Liabilities",
        "Common Stock": "Common Stock",
        "Retained Earnings": "Retained Earnings",
        "Total Stockholder Equity": "Shareholder Equity",
        "Total Liabilities And Stockholder Equity": "Liabilities + Equity"
    }, inplace=True)

    st.dataframe(df.style.format("{:.2f}"))

def show_cashflow_statement(cashflow_df):
    st.markdown("### 💸 Cash Flow Statement")

    line_items = [
        "Total Cash From Operating Activities",
        "Capital Expenditures",
        "Total Cashflows From Investing Activities",
        "Dividends Paid",
        "Repurchase Of Stock",
        "Total Cash From Financing Activities",
        "Effect Of Exchange Rate Changes",
        "Change In Cash",
        "Cash At End Of Period"
    ]

    existing = [item for item in line_items if item in cashflow_df.index]
    df = cashflow_df.loc[existing]

    df.rename(index={
        "Total Cash From Operating Activities": "Cash from Ops",
        "Capital Expenditures": "CapEx",
        "Total Cashflows From Investing Activities": "Cash from Investing",
        "Dividends Paid": "Dividends Paid",
        "Repurchase Of Stock": "Share Buybacks",
        "Total Cash From Financing Activities": "Cash from Financing",
        "Effect Of Exchange Rate Changes": "FX Impact",
        "Change In Cash": "Net Cash Flow",
        "Cash At End Of Period": "Ending Cash Balance"
    }, inplace=True)

    st.dataframe(df.style.format("{:.2f}"))

def show_financial_ratios(income_df, balance_df):
    st.markdown("### 📊 Key Financial Ratios")

    try:
        year = income_df.columns[-1]
        revenue = income_df.loc["Total Revenue", year] if "Total Revenue" in income_df.index else None
        net_income = income_df.loc["Net Income", year] if "Net Income" in income_df.index else None
        total_assets = balance_df.loc["Total Assets", year] if "Total Assets" in balance_df.index else None
        equity = balance_df.loc["Total Stockholder Equity", year] if "Total Stockholder Equity" in balance_df.index else None
        current_assets = balance_df.loc["Total Current Assets", year] if "Total Current Assets" in balance_df.index else None
        current_liabilities = balance_df.loc["Total Current Liabilities", year] if "Total Current Liabilities" in balance_df.index else None

        ratios = {}
        if net_income and revenue:
            ratios["Net Profit Margin (%)"] = round((net_income / revenue) * 100, 2)
        if net_income and total_assets:
            ratios["Return on Assets (ROA) (%)"] = round((net_income / total_assets) * 100, 2)
        if net_income and equity:
            ratios["Return on Equity (ROE) (%)"] = round((net_income / equity) * 100, 2)
        if current_assets and current_liabilities:
            ratios["Current Ratio"] = round(current_assets / current_liabilities, 2)

        df = pd.DataFrame.from_dict(ratios, orient='index', columns=[str(year)])
        df.index.name = "Ratio"
        st.dataframe(df)

    except Exception as e:
        st.error(f"Error calculating ratios: {e}")
