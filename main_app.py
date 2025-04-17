import streamlit as st
import yfinance as yf
from dcf_valuation import run_dcf
from price_chart import show_chart
from financials import show_financials

st.set_page_config(page_title="📈 Stock Analyzer", layout="wide")
st.title("📊 Stock Analyzer App")

# --- Company Search ---
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

# --- Load Data & Show Tabs ---
if ticker_symbol:
    ticker = yf.Ticker(ticker_symbol)

    tab1, tab2, tab3 = st.tabs(["💸 DCF Valuation", "📈 Price Chart", "📄 Financials"])

    # --- DCF Valuation ---
    with tab1:
        st.subheader("💸 DCF Valuation")

        growth_rate = st.slider("Growth Rate (%)", 0.0, 20.0, 10.0) / 100
        terminal_growth = st.slider("Terminal Growth Rate (%)", 0.0, 10.0, 4.0) / 100
        wacc = st.slider("Discount Rate / WACC (%)", 0.0, 20.0, 10.0) / 100

        try:
            cashflow = ticker.cashflow
            ocf = cashflow.loc["Operating Cash Flow"]
            capex = cashflow.loc["Capital Expenditure"]
            fcf = ocf + capex
            fcf = fcf.dropna()
            avg_fcf = fcf.iloc[:3].mean()

            forecast_years = 5
            future_fcfs = [avg_fcf * (1 + growth_rate) ** i for i in range(1, forecast_years + 1)]
            terminal_value = future_fcfs[-1] * (1 + terminal_growth) / (wacc - terminal_growth)
            discounted_fcfs = [f / (1 + wacc) ** i for i, f in enumerate(future_fcfs, start=1)]
            discounted_terminal = terminal_value / (1 + wacc) ** forecast_years
            enterprise_value = sum(discounted_fcfs) + discounted_terminal

            st.metric("Estimated Enterprise Value (INR)", f"₹{enterprise_value:,.2f}")

            fcf_df = pd.DataFrame({
                "Year": [f"Year {i}" for i in range(1, 6)],
                "Future FCF (₹ Crores)": np.round(np.array(future_fcfs) / 1e7, 2),
                "Discounted FCF (₹ Crores)": np.round(np.array(discounted_fcfs) / 1e7, 2)
            })
            st.dataframe(fcf_df.set_index("Year"))

            st.line_chart(fcf_df.set_index("Year")[["Future FCF (₹ Crores)", "Discounted FCF (₹ Crores)"]])

        except Exception as e:
            st.error(f"Error in DCF calculation: {e}")
