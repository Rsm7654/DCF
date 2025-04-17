import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd

# Set page config
st.set_page_config(page_title="Stock Analyzer", layout="wide")

st.title("📈 Stock Analysis App")

# --- Sidebar: Feature Selection ---
feature = st.sidebar.selectbox(
    "Select Feature",
    ["📊 DCF Valuation", "📈 Price Chart", "📄 Financials"]
)

# --- Search for Company ---
company_query = st.text_input("🔍 Search Company")

ticker_symbol = None
if company_query:
    try:
        search = yf.Search(company_query)
        quotes = search.quotes
        if quotes:
            options = [f"{q['shortname']} ({q['symbol']})" for q in quotes if 'shortname' in q]
            selection = st.selectbox("Select Company", options)
            ticker_symbol = selection.split('(')[-1].strip(')')
    except Exception as e:
        st.error(f"Search error: {e}")

# --- Tabs for each feature ---
if ticker_symbol:
    ticker = yf.Ticker(ticker_symbol)

    # Create tabs
    tabs = ["DCF Valuation", "Price Chart", "Financials"]
    tab = st.radio("Select Tab", tabs)

    if tab == "DCF Valuation":
        # DCF Valuation logic here
        st.subheader("💸 DCF Valuation")

        growth_rate = st.slider("Growth Rate (%)", 0.0, 20.0, 10.0) / 100
        terminal_growth = st.slider("Terminal Growth Rate (%)", 0.0, 10.0, 4.0) / 100
        wacc = st.slider("Discount Rate / WACC (%)", 0.0, 20.0, 10.0) / 100

        # Fetching Data for DCF
        try:
            cashflow = ticker.cashflow
            ocf = cashflow.loc["Operating Cash Flow"]
            capex = cashflow.loc["Capital Expenditure"]
            fcf = ocf + capex  # Free Cash Flow

            fcf = fcf.dropna()
            avg_fcf = fcf.iloc[:3].mean()

            forecast_years = 5
            future_fcfs = [avg_fcf * (1 + growth_rate) ** i for i in range(1, forecast_years + 1)]

            terminal_value = future_fcfs[-1] * (1 + terminal_growth) / (wacc - terminal_growth)
            discounted_fcfs = [fcf / (1 + wacc) ** i for i, fcf in enumerate(future_fcfs, start=1)]
            discounted_terminal = terminal_value / (1 + wacc) ** forecast_years

            enterprise_value = sum(discounted_fcfs) + discounted_terminal

            st.write(f"**Estimated Enterprise Value (INR):** ₹{enterprise_value:,.2f}")
            st.subheader("📉 Forecasted FCFs")
            fcf_df = pd.DataFrame({
                "Year": [f"Year {i}" for i in range(1, 6)],
                "Future FCF (₹)": future_fcfs,
                "Discounted FCF (₹)": discounted_fcfs
            })
            st.dataframe(fcf_df.set_index("Year"))

        except Exception as e:
            st.error(f"Error fetching or processing data for DCF: {e}")

    elif tab == "Price Chart":
        # Price Chart logic here
        st.subheader(f"📈 Stock Price Chart - {ticker_symbol}")
        hist = ticker.history(period="5y")
        st.line_chart(hist["Close"])

    elif tab == "Financials":
        # Financials logic here
        st.subheader(f"📄 Financial Statements - {ticker_symbol}")

        st.write("**Income Statement**")
        st.dataframe(ticker.financials.T)

        st.write("**Balance Sheet**")
        st.dataframe(ticker.balance_sheet.T)

        st.write("**Cash Flow**")
        st.dataframe(ticker.cashflow.T)

else:
    st.info("Please enter a company name to get started.")
