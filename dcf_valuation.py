import streamlit as st
import pandas as pd
import numpy as np

def run_dcf(ticker):
    st.subheader("💸 DCF Valuation (₹ in Crores)")

    # Sliders
    growth_rate = st.slider("Growth Rate (%)", 0.0, 20.0, 10.0) / 100
    terminal_growth = st.slider("Terminal Growth Rate (%)", 0.0, 10.0, 4.0) / 100
    wacc = st.slider("Discount Rate / WACC (%)", 0.0, 20.0, 10.0) / 100

    try:
        # Get cash flow data
        cashflow = ticker.cashflow
        ocf = cashflow.loc["Operating Cash Flow"]
        capex = cashflow.loc["Capital Expenditure"]
        fcf = ocf + capex  # CapEx is negative, so addition is correct
        fcf = fcf.dropna()
        avg_fcf = fcf.iloc[:3].mean()

        # Forecast future FCFs
        forecast_years = 5
        future_fcfs = [avg_fcf * (1 + growth_rate) ** i for i in range(1, forecast_years + 1)]
        terminal_value = future_fcfs[-1] * (1 + terminal_growth) / (wacc - terminal_growth)

        # Discount future FCFs
        discounted_fcfs = [f / (1 + wacc) ** i for i, f in enumerate(future_fcfs, start=1)]
        discounted_terminal = terminal_value / (1 + wacc) ** forecast_years
        enterprise_value = sum(discounted_fcfs) + discounted_terminal

        # Convert to ₹ Crores
        future_fcfs_cr = np.round(np.array(future_fcfs) / 1e7, 2)
        discounted_fcfs_cr = np.round(np.array(discounted_fcfs) / 1e7, 2)
        discounted_terminal_cr = discounted_terminal / 1e7
        enterprise_value_cr = enterprise_value / 1e7

        # Display results
        st.metric("Estimated Enterprise Value", f"₹ {enterprise_value_cr:,.2f} Cr")

        fcf_df = pd.DataFrame({
            "Year": [f"Year {i}" for i in range(1, 6)],
            "Future FCF (₹ Cr)": future_fcfs_cr,
            "Discounted FCF (₹ Cr)": discounted_fcfs_cr
        })
        st.dataframe(fcf_df.set_index("Year"))

        st.line_chart(fcf_df.set_index("Year")[["Future FCF (₹ Cr)", "Discounted FCF (₹ Cr)"]])

        st.write(f"📌 **Discounted Terminal Value**: ₹ {discounted_terminal_cr:,.2f} Cr")
        st.write(f"📌 **Sum of Discounted FCFs**: ₹ {sum(discounted_fcfs_cr):,.2f} Cr")
        st.write("📌 **Enterprise Value = DCFs + Terminal Value**")

    except Exception as e:
        st.error(f"Error in DCF calculation: {e}")
