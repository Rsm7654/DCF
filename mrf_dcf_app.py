import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd

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

# --- Load ticker data ---
if ticker_symbol:
    ticker = yf.Ticker(ticker_symbol)

    if feature == "📊 DCF Valuation":
        st.subheader(f"💸 DCF Valuation - {ticker_symbol}")

        # --- User Inputs ---
        growth_rate = st.slider("Growth Rate (%)", 0.0, 20.0, 10.0) / 100
        terminal_growth = st.slider("Terminal Growth Rate (%)", 0.0, 10.0, 4.0) / 100
        wacc = st.slider("Discount Rate / WACC (%)", 0.0, 20.0, 10.0) / 100

        try:
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
            discounted_fcfs = [fcf / (1 + wacc) ** i for i, fcf in enumerate(future_fcfs, 1)]
            discounted_terminal = terminal_value / (1 + wacc) ** forecast_years

            # --- Valuation ---
            enterprise_value = sum(discounted_fcfs) + discounted_terminal

            st.markdown(f"### 📌 Estimated Enterprise Value: ₹{enterprise_value:,.2f}")

            # --- FCF Table ---
            fcf_df = pd.DataFrame({
                "Year": [f"Year {i}" for i in range(1, forecast_years + 1)],
                "Future FCF (₹)": future_fcfs,
                "Discounted FCF (₹)": discounted_fcfs
            })
            st.dataframe(fcf_df.set_index("Year"))

        except Exception as e:
            st.error(f"Error in DCF calculation: {e}")

    elif feature == "📈 Price Chart":
        st.subheader(f"📈 Stock Price Chart - {ticker_symbol}")
        hist = ticker.history(period="5y")
        st.line_chart(hist["Close"])

    elif feature == "📄 Financials":
        st.subheader(f"📄 Financial Statements - {ticker_symbol}")
        st.write("**Income Statement**")
        st.dataframe(ticker.financials.T)

        st.write("**Balance Sheet**")
        st.dataframe(ticker.balance_sheet.T)

        st.write("**Cash Flow**")
        st.dataframe(ticker.cashflow.T)
