# peer_comparison.py

import streamlit as st
import pandas as pd

def peer_comparison(ticker_symbol, df_stocks):
    # Get the company row based on the selected ticker
    company_row = df_stocks[df_stocks['Ticker'] == ticker_symbol]
    
    if not company_row.empty and 'Sector' in df_stocks.columns:
        selected_sector = company_row.iloc[0]['Sector']
        st.subheader(f"🧩 Peer Comparison in {selected_sector} Sector")

        peers = df_stocks[df_stocks['Sector'] == selected_sector]

        if not peers.empty:
            # Show the table of peers (with relevant columns)
            st.dataframe(peers[['Company', 'Ticker', 'Sector', 'MarketCap', 'P/E', 'EPS']].sort_values(by='MarketCap', ascending=False))

            # Optional: plot bar chart of market cap
            st.bar_chart(peers.set_index('Company')['MarketCap'])
        else:
            st.info("No peers found in the same sector.")
