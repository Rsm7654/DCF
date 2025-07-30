import streamlit as st
import yfinance as yf
import pandas as pd

def peer_comparison(ticker_symbol, df_stocks):
    try:
        ticker = yf.Ticker(ticker_symbol)
        sector = ticker.info.get("sector", None)

        if not sector:
            st.warning("⚠️ Could not retrieve sector information from the ticker.")
            return

        st.info(f"📌 Identified Sector: {sector}")

        peer_data = []
        for symbol in df_stocks["Ticker"].dropna().unique():
            try:
                peer_ticker = yf.Ticker(symbol)
                info = peer_ticker.info

                if info.get("sector") == sector:
                    peer_data.append({
                        "Company": info.get("shortName", symbol),
                        "Ticker": symbol,
                        "Sector": info.get("sector", "N/A"),
                        "Price": info.get("currentPrice", None),
                        "Market Cap": info.get("marketCap", None),
                        "P/E Ratio": info.get("trailingPE", None)
                    })
            except Exception:
                continue

        if peer_data:
            df_peer = pd.DataFrame(peer_data)
            st.dataframe(df_peer.set_index("Ticker"))
        else:
            st.info("No peer companies found in the same sector.")

    except Exception as e:
        st.error(f"Error fetching peer data: {e}")
