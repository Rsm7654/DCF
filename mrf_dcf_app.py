import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd

st.title("💸 DCF Valuation Model")

# --- Search for Company ---
company_query = st.text_input("🔍 Enter Company Name", value="MRF")

ticker_symbol = None  # default

if company_query:
    search = yf.Search(company_query)
    quotes = search.quotes

    if quotes:
        # Create dropdown options: "Company Name (Ticker)"
        options = [f"{item['shortname']} ({item['symbol']})" for item in quotes if 'shortname' in item and 'symbol' in item]
        selection = st.selectbox("Select a Company", options)
        ticker_symbol = selection.split('(')[-1].strip(')')
    else:
        st.warning("No matching companies found.")

# --- If a valid symbol is selected ---
if ticker_symbol:
    # --- User Inputs ---
    growth_rate = st.slider("Growth Rate (%)", 0.0, 20.0, 10.0) / 100
    terminal_growth = st.slider("Terminal Growth Rate (%)", 0.0, 10.0, 4.0) / 100
    wacc = st.slider("Discount Rate / WACC (%)", 0.0, 20.0, 10.0) / 100

    # --- Fetching and Calculating DCF ---
    try:
        ticker = yf.Ticker(ticker_symbol)
        cashflow = ticker.cashflow

        # Rename to match available index
        ocf = cashflow.loc["Operating Cash Flow"]
        capex = cashflow.loc["Capital Expenditure"]
        fcf = ocf + capex  # Free Cash Flow

        fcf = fcf.dropna()
        avg_fcf = fcf.iloc[:3].mean()

        # Forecast FCFs for 5 years
        forecast_years = 5
        future_fcfs = [avg_fcf * (1 + growth_rate) ** i for i in range(1, forecast_years + 1)]

        # Terminal Value
        terminal_value = future_fcfs[-1] * (1 + terminal_growth) / (wacc - terminal_growth)

        # Discount FCFs
        discounted_fcfs = [fcf / (1 + wacc) ** i for i, fcf in enumerate(future_fcfs, start=1)]
        discounted_terminal = terminal_value / (1 + wacc) ** forecast_years

        # Valuation
        enterprise_value = sum(discounted_fcfs) + discounted_terminal

        # --- Display Results ---
        st.subheader("📊 Valuation Result")
        st.success(f"**Estimated Enterprise Value (INR):** ₹{enterprise_value:,.2f}")

        st.subheader("📉 Forecasted FCFs")
        fcf_df = pd.DataFrame({
            "Year": [f"Year {i}" for i in range(1, 6)],
            "Future FCF (₹)": future_fcfs,
            "Discounted FCF (₹)": discounted_fcfs
        })
        st.dataframe(fcf_df.set_index("Year"))

    except Exception as e:
        st.error(f"Error fetching or processing data: {e}")
