import streamlit as st
import pandas as pd
import yfinance as yf

def fetch_sector(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        if info is None:
            st.error(f"Failed to fetch data for {ticker_symbol}. It might be an invalid ticker.")
            return None
        
        # Check if 'sector' exists in the fetched info
        sector = info.get('sector', None)
        if sector is None:
            st.warning(f"Sector information not available for {ticker_symbol}")
        return sector
    except Exception as e:
        st.error(f"Error fetching sector for {ticker_symbol}: {e}")
        return None

def update_sector_info(df_stocks):
    # Fetch sector information for all stocks if the sector is missing
    if 'Sector' not in df_stocks.columns:
        st.warning("Sector column is missing. Fetching sector data from Yahoo Finance.")
        df_stocks['Sector'] = df_stocks['Ticker'].apply(fetch_sector)
    return df_stocks

def peer_comparison(ticker_symbol, df_stocks):
    # Update sector info before performing comparison
    df_stocks = update_sector_info(df_stocks)
    
    # Get the company row based on the selected ticker
    company_row = df_stocks[df_stocks['Ticker'] == ticker_symbol]
    
    if company_row.empty:
        st.warning(f"No data found for ticker: {ticker_symbol}")
        return

    # Display the sector of the selected company
    selected_sector = company_row.iloc[0]['Sector']
    if selected_sector is None:
        st.warning(f"The selected company ({ticker_symbol}) does not have a sector listed.")
        return

    st.write(f"Selected company sector: {selected_sector}")
    st.subheader(f"🧩 Peer Comparison in {selected_sector} Sector")

    # Get peers in the same sector
    peers = df_stocks[df_stocks['Sector'] == selected_sector]

    # Show the number of companies in the sector
    st.write(f"Found {len(peers)} peers in the {selected_sector} sector.")

    if not peers.empty:
        # Show the table of peers (with relevant columns)
        st.dataframe(peers[['Company', 'Ticker', 'Sector', 'MarketCap', 'P/E', 'EPS']].sort_values(by='MarketCap', ascending=False))

        # Optional: plot bar chart of market cap
        st.bar_chart(peers.set_index('Company')['MarketCap'])

        # Optional: plot P/E ratio comparison
        st.subheader("P/E Ratio Comparison")
        st.bar_chart(peers.set_index('Company')['P/E'])

        # Optional: plot EPS comparison
        st.subheader("EPS Comparison")
        st.bar_chart(peers.set_index('Company')['EPS'])

    else:
        st.info("No peers found in the same sector.")

