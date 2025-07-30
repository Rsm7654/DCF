import streamlit as st
import pandas as pd
import numpy as np

def run_dcf(ticker):
    st.subheader("💸 DCF Valuation (₹ in Crores)")

    # Sliders
    growth_rate = st.slider("Growth Rate (%)", 0.0, 20.0, 10.0) / 100
    terminal_growth = st.slider("Terminal Growth Rate (%)", 0.0, 10.0, 4.0) / 100
    wacc = st.slider("Discount Rate / WACC (%)", 0.0, 20.0, 10.0) / 100
    forecast_years = st.slider("Forecast Years", 3, 10, 5)

    try:
        # Get cash flow data
        cashflow = ticker.cashflow

        ocf = cashflow.loc["Operating Cash Flow"] if "Operating Cash Flow" in cashflow.index else None
        capex = cashflow.loc["Capital Expenditure"] if "Capital Expenditure" in cashflow.index else None

        if ocf is None or capex is None:
            st.error("⚠️ Required data ('Operating Cash Flow' or 'Capital Expenditure') is missing.")
            return

        fcf = ocf + capex  # CapEx is usually negative, so this adds correctly
        fcf = fcf.dropna()

        if fcf.empty:
            st.error("⚠️ No valid Free Cash Flow data available.")
            return

        avg_fcf = fcf.iloc[:min(3, len(fcf))].mean()

        if wacc <= terminal_growth:
            st.error("⚠️ WACC must be greater than Terminal Growth Rate.")
            return

        # Forecast future FCFs
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
        st.metric("💰 Estimated Enterprise Value", f"₹ {enterprise_value_cr:,.2f} Cr")

        fcf_df = pd.DataFrame({
            "Year": [f"Year {i}" for i in range(1, forecast_years + 1)],
            "Future FCF (₹ Cr)": future_fcfs_cr,
            "Discounted FCF (₹ Cr)": discounted_fcfs_cr
        }).set_index("Year")

        st.dataframe(fcf_df)
        st.line_chart(fcf_df)

        st.write(f"📌 **Discounted Terminal Value**: ₹ {discounted_terminal_cr:,.2f} Cr")
        st.write(f"📌 **Sum of Discounted FCFs**: ₹ {sum(discounted_fcfs_cr):,.2f} Cr")
        st.write("📌 **Enterprise Value = DCFs + Terminal Value**")

        # Estimate fair value per share
        try:
            balance_sheet = ticker.balance_sheet
            cash = balance_sheet.loc["Cash And Cash Equivalents"].iloc[0] if "Cash And Cash Equivalents" in balance_sheet.index else 0
            debt = balance_sheet.loc["Total Debt"].iloc[0] if "Total Debt" in balance_sheet.index else 0
            shares_outstanding = ticker.info.get("sharesOutstanding", 0)

            if shares_outstanding and shares_outstanding > 0:
                equity_value = enterprise_value + cash - debt
                fair_value_per_share = equity_value / shares_outstanding
                fair_value_rs = fair_value_per_share  # already ₹

                st.metric("📈 Estimated Fair Value per Share", f"₹ {fair_value_rs:,.2f}")
            else:
                st.warning("⚠️ Shares outstanding not available to estimate fair value per share.")
        except Exception as e:
            st.warning(f"⚠️ Fair value per share could not be calculated: {e}")

    except Exception as e:
        st.exception(e)
