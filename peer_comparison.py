import streamlit as st
import yfinance as yf
import pandas as pd

def peer_comparison(selected_ticker, df_stocks):
    try:
        # Check if 'Sector' and 'Ticker' columns are available
        required_cols = ['Ticker', 'Sector']
        missing = [col for col in required_cols if col not in df_stocks.columns]
        if missing:
            st.error(f"❌ Missing columns in stock list: {', '.join(missing)}")
            return

        # Get the sector of the selected ticker
        selected_row = df_stocks[df_stocks["Ticker"] == selected_ticker]
        if selected_row.empty:
            st.warning("⚠️ Ticker not found in stock list.")
            return

        sector = selected_row["Sector"].values[0]

        # Filter peers from the same sector
        peer_tickers = df_stocks[df_stocks["Sector"] == sector]["Ticker"].tolist()

        st.subheader(f"📊 Peer Comparison in Sector: {sector}")
        comparison_data = []

        for ticker in peer_tickers:
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
                    "Profit Margin": info.get("profitMargins")
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
