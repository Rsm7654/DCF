import streamlit as st

def show_chart(ticker):
    symbol = ticker.ticker.upper() if hasattr(ticker, "ticker") else "Stock"
    st.subheader(f"📈 Stock Price Chart – {symbol}")

    try:
        hist = ticker.history(period="5y")

        if hist.empty:
            st.warning("⚠️ No historical price data available.")
            return

        st.line_chart(hist["Close"], use_container_width=True)
        st.caption("Showing 5 years of closing price data.")
        
    except Exception as e:
        st.error(f"Error fetching historical data: {e}")
