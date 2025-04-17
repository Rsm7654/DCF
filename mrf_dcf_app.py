import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd

st.title("💸 DCF Valuation Model")

# --- Company Search ---
company_query = st.text_input("🔍 Search by Company Name")

ticker_symbol = None

if company_query:
    try:
        search = yf.utils.get_json("https://query2.finance.yahoo.com/v1/finance/search", params={"q": company_query})
        quotes = search.get("quotes", [])
        if quotes:
            options = [f"{item['shortname']} ({item['symbol']})" for item in quotes if "shortname" in item and "symbol" in item]
            selection = st.selectbox("Select a company", options)
            ticker_symbol = selection.split('(')[-1].strip(')')
        else:
            st.warning("No matching companies found.")
    except Exception as e:
        st.error(f"Search error: {e}")

# --- Proceed if valid ticker is selected ---
if ticker_symbol:
    # --- User Inputs ---
    growth_rate = st.slider("Growth Rate (%)", 0.0, 20.0, 10.0) / 100
    terminal_growth = st.slider("Terminal Growth Rate (%)", 0.0, 10.0, 4.0) / 100
    wacc = st.slider("Discount Rate / WACC (%)", 0.0, 20.0, 10.0) / 100

    # --- Fetching Data ---
    try:
        ticker = yf.Ticker(ticker_symbol)
        cashflow = ticker.cashflow

        ocf = cashflow.loc["Operating Cash Flow"]
        capex = cashflow.loc["Capital Expenditure"]
        fcf = ocf + capex  # Free Cash Flow

        fcf = fcf.dropna()
        avg_fcf = fcf.iloc[:3].mean()

        # --- Forecast FCFs ---
        forecast_years = 5
        future_fcfs = [avg_fcf * (1 + growth_rate) ** i for i in range(1, forecast_years + 1)]

        # --- Terminal Value ---
        terminal_value = future_fcfs[-1] * (1 + terminal_growth) / (wacc - terminal_growth)

        # --- Discounting ---
        discounted_fcfs = [fcf / (1 + wacc) ** i for i, fcf in enumerate(future_fcfs, start=1)]
        discounted_terminal = terminal_value / (1 + wacc) ** forecast_years

        # --- Valuation ---
        enterprise_value = sum(discounted_fcfs) + discounted_terminal

        st.subheader("📊 Valuation Result")
        st.write(f"**Estimated Enterprise Value (INR):** ₹{enterprise_value:,.2f}")

        st.subheader("📉 Forecasted FCFs")
        fcf_df = pd.DataFrame({
            "Year": [f"Year {i}" for i in range(1, 6)],
            "Future FCF (₹)": future_fcfs,
            "Discounted FCF (₹)": discounted_fcfs
        })
        st.dataframe(fcf_df.set_index("Year"))

    except Exception as e:
        st.error(f"Error fetching or processing data: {e}")
