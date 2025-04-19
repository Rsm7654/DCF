# peer_comparison.py

import streamlit as st
import pandas as pd

def peer_comparison(ticker_symbol, df_stocks):
    # Check if the 'Sector' column exists and is populated
    if 'Sector' not in df_stocks.columns:
        st.error("Sector column is missing in the dataset.")
        return

    # Get the company row based on the selected ticker
    company_row = df_stocks[df_stocks['Ticker'] == ticker_symbol]
    
    if company_row.empty:
        st.warning(f"No data found for ticker: {ticker_symbol}")
        return

    # Debugging: Display the sector of the selected company
    selected_sector = company_row.iloc[0]['Sector']
    st.write(f"Selected company sector: {selected_sector}")

    st.subheader(f"🧩 Peer Comparison in {selected_sector} Sector")

    # Get peers in the same sector
    peers = df_stocks[df_stocks['Sector'] == selected_sector]

    # Debugging: Show the number of companies in the sector
    st.write(f"Found {len(peers)} peers in the {selected_sector} sector.")

    if not peers.empty:
        # Show the table of peers (with relevant columns)
        st.dataframe(peers[['Company', 'Ticker', 'Sector', 'MarketCap', 'P/E', 'EPS']].sort_values(by='MarketCap', ascending=False))

        # Optional: plot bar chart of market cap
        st.bar_chart(peers.set_index('Company')['MarketCap'])
    else:
        st.info("No peers found in the same sector.")
