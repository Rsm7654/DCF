import streamlit as st
import yfinance as yf
import pandas as pd

# Function to extract sector from Yahoo Finance
def get_sector_from_yf(ticker_symbol):
    try:
        # Fetch the stock data
        stock = yf.Ticker(ticker_symbol)

        # Extract the sector from the info dictionary
        sector = stock.info.get("sector", "Sector not available")
        return sector
    except Exception as e:
        st.warning(f"⚠️ Error fetching sector for {ticker_symbol}: {e}")
        return None

def peer_comparison(selected_ticker, df_stocks):
    try:
        # Check if 'Ticker' column is available
        if 'Ticker' not in df_stocks.columns:
            st.error("❌ 'Ticker' column is missing in the stock list.")
            return

        # Get the sector of the selected ticker from Yahoo Finance
        selected_sector = get_sector_from_yf(selected_ticker)
        if not selected_sector:
            st.warning(f"⚠️ Could not fetch sector for {selected_ticker}.")
            return

        # Filter peers from the same sector (dynamically fetch sector for each peer)
        peer_tickers = df_stocks['Ticker'].tolist()
        
        st.subheader(f"📊 Peer Comparison for Sector: {selected_sector}")
        comparison_data = []

        for ticker in peer_tickers:
            # Fetch sector dynamically for each ticker
            peer_sector = get_sector_from_yf(ticker)
            
            if peer_sector and peer_sector == selected_sector:
                try:
                    stock = yf.Ticker(ticker)
                    info = stock.info

                    if info is None or "shortName" not in info:
                        continue  # skip if data is incomplete or broken

                    comparison_data.append({
                        "Company": info.get("shortName", ticker),
                        "Ticker": ticker,
                        "Market Cap": info.get("marketCap"),
                        "P/E Ratio": info.get("trailingPE"),
                        "Return on Equity": info.get("returnOnEquity"),
                        "Profit Margin": info.get("profitMargins"),
                    })
                except Exception as e:
                    st.warning(f"⚠️ Could not fetch data for {ticker}: {e}")
                    continue

        if comparison_data:
            df_comparison = pd.DataFrame(comparison_data)
            st.dataframe(df_comparison)
        else:
            st.info("No valid peer data available to compare.")

    except Exception as e:
        st.error(f"An error occurred in peer comparison: {e}")
