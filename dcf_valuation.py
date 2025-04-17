import streamlit as st
import numpy as np
import pandas as pd

def run_dcf(ticker, symbol):
    st.subheader(f"💸 DCF Valuation - {symbol}")

    try:
        cashflow = ticker.cashflow
        ocf = cashflow.loc["Operating Cash Flow"]
        capex = cashflow.loc["Capital Expenditure"]
        fcf = ocf + capex
        fcf = fcf.dropna()
        avg_fcf = fcf.iloc[:3].mean()

        growth_rate = st.slider("Growth Rate (%)", 0.0, 20.0, 10.0) / 100
        terminal_growth = st.slider("Terminal Growth Rate (%)", 0.0, 10.0, 4.0) / 100
        wacc = st.slider("Discount Rate / WACC (%)", 0.0, 20.0, 10.0) / 100

        forecast_years = 5
        future_fcfs = [avg_fcf * (1 + growth_rate) ** i for i in range(1, forecast_years + 1)]
        terminal_value = future_fcfs[-1] * (1 + terminal_growth) / (wacc - terminal_growth)

        discounted_fcfs = [fcf / (1 + wacc) ** i for i, fcf in enumerate(future_fcfs, start=1)]
        discounted_terminal = terminal_value / (1 + wacc) ** forecast_years

        enterprise_value = sum(discounted_fcfs) + discounted_terminal

        st.write(f"**Estimated Enterprise Value (INR):** ₹{enterprise_value:,.2f}")
        st.subheader("📉 Forecasted FCFs")
        df = pd.DataFrame({
            "Year": [f"Year {i}" for i in range(1, 6)],
            "Future FCF (₹)": future_fcfs,
            "Discounted FCF (₹)": discounted_fcfs
        })
        st.dataframe(df.set_index("Year"))

    except Exception as e:
        st.error(f"DCF calculation error: {e}")
