import streamlit as st
import pandas as pd
import yfinance as yf

@st.cache_data(show_spinner=False)
def fetch_stock_info(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            "Ticker": ticker,
            "Company": info.get("shortName", ticker),
            "Sector": info.get("sector"),
            "MarketCap": info.get("marketCap"),
            "P/E": info.get("trailingPE"),
            "EPS": info.get("trailingEps")
        }
    except Exception as e:
        st.warning(f"Could not fetch data for {ticker}: {e}")
        return None

def peer_comparison(ticker_symbol, df_stocks):
    st.subheader("📊 Peer-to-Peer Comparison")

    # Get list of tickers from your stock list
    tickers = df_stocks["Ticker"].dropna().unique().tolist()

    # Fetch all stock info
    with st.spinner("Fetching peer data..."):
        stock_data = [fetch_stock_info(ticker) for ticker in tickers]
        df_peers = pd.DataFrame([data for data in stock_data if data])

    if df_peers.empty:
        st.error("No stock data could be fetched.")
        return

    # Get selected company info
    selected_company = df_peers[df_peers["Ticker"] == ticker_symbol]
    if selected_company.empty:
        st.error(f"No data found for selected ticker: {ticker_symbol}")
        return

    sector = selected_company.iloc[0]["Sector"]
    st.markdown(f"**Selected Company**: `{ticker_symbol}` | **Sector**: `{sector}`")

    # Filter peers from the same sector
    sector_peers = df_peers[df_peers["Sector"] == sector]

    if sector_peers.empty:
        st.warning("No peers found in the same sector.")
        return

    st.write(f"✅ Found **{len(sector_peers)}** peers in sector `{sector}`")

    # Show table
    st.dataframe(sector_peers[['Company', 'Ticker', 'MarketCap', 'P/E', 'EPS']].sort_values(by='MarketCap', ascending=False))

    # Charts
    st.subheader("📈 Market Cap Comparison")
    st.bar_chart(sector_peers.set_index("Company")["MarketCap"])

    st.subheader("📉 P/E Ratio Comparison")
    st.bar_chart(sector_peers.set_index("Company")["P/E"])

    st.subheader("💵 EPS Comparison")
    st.bar_chart(sector_peers.set_index("Company")["EPS"])

# Example usage (assuming you have a DataFrame df_stocks and a ticker_symbol)
# peer_comparison(ticker_symbol, df_stocks)
